/*
 *   Copyright (C) 2015,2016 by Jonathan Naylor G4KLX
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

#if !defined(YSFRX_H)
#define  YSFRX_H

#include "Config.h"
#include "YSFDefines.h"

enum YSFRX_STATE {
  YSFRXS_NONE,
  YSFRXS_DATA
};

class CYSFRX {
public:
  CYSFRX();

  void samples(const q15_t* samples, uint8_t length);

  void reset();

private:
  YSFRX_STATE m_state;
  uint32_t    m_bits[YSF_RADIO_SYMBOL_LENGTH];
  q15_t       m_samples[YSF_FRAME_LENGTH_SAMPLES];
  uint16_t    m_bitPtr;
  uint16_t    m_samplePtr;
  uint16_t    m_syncPtr;
  uint16_t    m_syncStartPtr;
  uint16_t    m_syncEndPtr;
  uint16_t    m_endPtr;
  uint16_t    m_lostCount;
  q31_t       m_maxCorr;
  q15_t       m_centre[4U];
  q15_t       m_threshold[4U];
  uint8_t     m_averagePtr;

  void process(q15_t sample);
  void processData();
  void processSync();
};

#endif

