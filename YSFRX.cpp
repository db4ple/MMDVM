/*
 *   Copyright (C) 2009-2016 by Jonathan Naylor G4KLX
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#define  WANT_DEBUG

#include "Config.h"
#include "Globals.h"
#include "YSFRX.h"
#include "Utils.h"

const unsigned int BUFFER_LENGTH = 200U;

const q15_t SCALING_FACTOR = 18750;      // Q15(0.55)

const uint8_t SYNC_SYMBOL_ERRS = 0U;

const uint8_t SYNC_BIT_START_ERRS = 2U;
const uint8_t SYNC_BIT_RUN_ERRS   = 4U;

const unsigned int MAX_SYNC_FRAMES = 4U + 1U;

const uint8_t BIT_MASK_TABLE[] = {0x80U, 0x40U, 0x20U, 0x10U, 0x08U, 0x04U, 0x02U, 0x01U};

#define WRITE_BIT1(p,i,b) p[(i)>>3] = (b) ? (p[(i)>>3] | BIT_MASK_TABLE[(i)&7]) : (p[(i)>>3] & ~BIT_MASK_TABLE[(i)&7])
#define READ_BIT1(p,i)    (p[(i)>>3] & BIT_MASK_TABLE[(i)&7])

CYSFRX::CYSFRX() :
m_state(YSFRXS_NONE),
m_bits(),
m_samples(),
m_bitPtr(0U),
m_samplePtr(0U),
m_syncPtr(0U),
m_syncStartPtr(0U),
m_syncEndPtr(0U),
m_endPtr(0U),
m_lostCount(0U),
m_maxCorr(0),
m_centre(),
m_threshold(),
m_averagePtr(0U)
{
}

void CYSFRX::reset()
{
  m_state        = YSFRXS_NONE;
  m_bitPtr       = 0U;
  m_samplePtr    = 0U;
  m_syncPtr      = 0U;
  m_syncStartPtr = 0U;
  m_syncEndPtr   = 0U;
  m_endPtr       = 0U;
  m_lostCount    = 0U;
  m_maxCorr      = 0;
  m_averagePtr   = 0U;
}

void CYSFRX::samples(const q15_t* samples, uint8_t length)
{
  for (uint16_t i = 0U; i < length; i++)
    process(samples[i]);
}

void CYSFRX::process(q15_t sample)
{
  m_bits[m_bitPtr] <<= 1;
  if (sample < 0)
    m_bits[m_bitPtr] |= 0x01U;

  m_samples[m_samplePtr] = sample;

  if (m_state == YSFRXS_NONE) {
    processSync();
  } else {
    if (m_samplePtr >= m_syncStartPtr && m_samplePtr <= m_syncEndPtr)
      processSync();

    if (m_samplePtr == m_endPtr)
      processData();
  }

  m_bitPtr++;
  if (m_bitPtr >= YSF_RADIO_SYMBOL_LENGTH)
    m_bitPtr = 0U;

  m_samplePtr++;
  if (m_samplePtr >= YSF_FRAME_LENGTH_SAMPLES)
    m_samplePtr = 0U;
}

void CYSFRX::processData()
{
  // We've not seen a data sync for too long, signal RXLOST and change to RX_NONE
  m_lostCount--;
  if (m_lostCount == 0U) {
    DEBUG1("YSFRX: sync timed out, lost lock");

    io.setDecode(false);
    io.setADCDetection(false);

    serial.writeYSFLost();

    m_state        = YSFRXS_NONE;
    m_syncPtr      = 0U;
    m_syncStartPtr = 0U;
    m_syncEndPtr   = 0U;
    m_endPtr       = 0U;
    m_maxCorr      = 0;

    return;
  }

  uint8_t buffer[YSF_FRAME_LENGTH_BYTES + 1U];

  buffer[0U] = m_lostCount == (MAX_SYNC_FRAMES - 1U) ? 0x01U : 0x00U;

  // Find the average centre and threshold values
  q15_t centre    = (m_centre[0U]    + m_centre[1U]    + m_centre[2U]    + m_centre[3U])    >> 2;
  q15_t threshold = (m_threshold[0U] + m_threshold[1U] + m_threshold[2U] + m_threshold[3U]) >> 2;

  uint16_t ptr = m_endPtr + YSF_RADIO_SYMBOL_LENGTH;
  if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
    ptr -= YSF_FRAME_LENGTH_SAMPLES;

  uint16_t bufferPtr = 8U;
  for (uint16_t i = 0U; i < YSF_FRAME_LENGTH_BITS; i += 2U) {
    q15_t sample = m_samples[ptr] - centre;

    if (sample < -threshold) {
      WRITE_BIT1(buffer, bufferPtr, false);
      bufferPtr++;
      WRITE_BIT1(buffer, bufferPtr, true);
      bufferPtr++;
    } else if (sample < 0) {
      WRITE_BIT1(buffer, bufferPtr, false);
      bufferPtr++;
      WRITE_BIT1(buffer, bufferPtr, false);
      bufferPtr++;
    } else if (sample < threshold) {
      WRITE_BIT1(buffer, bufferPtr, true);
      bufferPtr++;
      WRITE_BIT1(buffer, bufferPtr, false);
      bufferPtr++;
    } else {
      WRITE_BIT1(buffer, bufferPtr, true);
      bufferPtr++;
      WRITE_BIT1(buffer, bufferPtr, true);
      bufferPtr++;
    }

    ptr += YSF_RADIO_SYMBOL_LENGTH;
    if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
      ptr -= YSF_FRAME_LENGTH_SAMPLES;
  }

  serial.writeYSFData(buffer, YSF_FRAME_LENGTH_BYTES + 1U);

  // Reset synchronisation values
  m_maxCorr = 0;
}

void CYSFRX::processSync()
{
  // Fuzzy matching of the data sync bit sequence
  if (countBits32((m_bits[m_bitPtr] & YSF_SYNC_SYMBOLS_MASK) ^ YSF_SYNC_SYMBOLS) > SYNC_SYMBOL_ERRS)
    return;

  uint16_t ptr = m_samplePtr + YSF_FRAME_LENGTH_SAMPLES - YSF_SYNC_LENGTH_SAMPLES + YSF_RADIO_SYMBOL_LENGTH;
  if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
    ptr -= YSF_FRAME_LENGTH_SAMPLES;

  q31_t corr = 0;
  q15_t max  = -16000;
  q15_t min  =  16000;

  uint32_t mask = 0x00080000U;
  for (uint8_t i = 0U; i < YSF_SYNC_LENGTH_SYMBOLS; i++, mask >>= 1) {
    bool b = (YSF_SYNC_SYMBOLS & mask) == mask;

    if (m_samples[ptr] > max)
      max = m_samples[ptr];
    if (m_samples[ptr] < min)
      min = m_samples[ptr];

    corr += b ? -m_samples[ptr] : m_samples[ptr];

    ptr += YSF_RADIO_SYMBOL_LENGTH;
    if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
      ptr -= YSF_FRAME_LENGTH_SAMPLES;
  }

  q15_t centre = (max + min) >> 1;

  q31_t v1 = (max - centre) * SCALING_FACTOR;
  q15_t threshold = q15_t(v1 >> 15);

  ptr = m_samplePtr + YSF_FRAME_LENGTH_SAMPLES - YSF_SYNC_LENGTH_SAMPLES + YSF_RADIO_SYMBOL_LENGTH;
  if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
    ptr -= YSF_FRAME_LENGTH_SAMPLES;

  uint64_t sync = 0x00U;
  for (uint8_t i = 0U; i < YSF_SYNC_LENGTH_SYMBOLS; i++) {
    q15_t sample = m_samples[ptr] - centre;

    if (sample < -threshold) {
      sync <<= 2;
      sync |= 0x01U;
    } else if (sample < 0) {
      sync <<= 2;
      sync |= 0x00U;
    } else if (sample < threshold) {
      sync <<= 2;
      sync |= 0x02U;
    } else {
      sync <<= 2;
      sync |= 0x03U;
    }

    ptr += YSF_RADIO_SYMBOL_LENGTH;
    if (ptr >= YSF_FRAME_LENGTH_SAMPLES)
      ptr -= YSF_FRAME_LENGTH_SAMPLES;
  }

  // Fuzzy matching of the data sync bit sequence
  if (m_state == YSFRXS_NONE) {
    if (countBits64((sync & YSF_SYNC_BITS_MASK) ^ YSF_SYNC_BITS) > SYNC_BIT_START_ERRS)
      return;

    if (corr <= m_maxCorr)
      return;

    DEBUG3("YSFRX: sync found with centre/threshold", centre, threshold);

    m_threshold[0U] = m_threshold[1U] = m_threshold[2U] = m_threshold[3U] = threshold;
    m_centre[0U]    = m_centre[1U]    = m_centre[2U]    = m_centre[3U]    = centre;
    m_averagePtr    = 0U;

    m_state = YSFRXS_DATA;

    io.setDecode(true);
    io.setADCDetection(true);
  } else {
    if (countBits64((sync & YSF_SYNC_BITS_MASK) ^ YSF_SYNC_BITS) > SYNC_BIT_RUN_ERRS)
      return;

    if (corr <= m_maxCorr)
      return;

    DEBUG4("YSFRX: sync found at pos/centre/threshold", m_samplePtr - m_syncPtr, centre, threshold);

    m_threshold[m_averagePtr] = threshold;
    m_centre[m_averagePtr]    = centre;

    m_averagePtr++;
    if (m_averagePtr >= 4U)
      m_averagePtr = 0U;
  }

  m_maxCorr   = corr;
  m_lostCount = MAX_SYNC_FRAMES;
  m_syncPtr   = m_samplePtr;

  m_syncStartPtr = m_syncPtr + YSF_FRAME_LENGTH_SAMPLES - 2U;
  if (m_syncStartPtr >= YSF_FRAME_LENGTH_SAMPLES)
    m_syncStartPtr -= YSF_FRAME_LENGTH_SAMPLES;

  m_syncEndPtr = m_syncPtr + 2U;
  if (m_syncEndPtr >= YSF_FRAME_LENGTH_SAMPLES)
    m_syncEndPtr -= YSF_FRAME_LENGTH_SAMPLES;

  m_endPtr = m_samplePtr + YSF_FRAME_LENGTH_SAMPLES - YSF_SYNC_LENGTH_SAMPLES;
  if (m_endPtr >= YSF_FRAME_LENGTH_SAMPLES)
    m_endPtr -= YSF_FRAME_LENGTH_SAMPLES;
}

