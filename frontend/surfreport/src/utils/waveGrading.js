// src/utils/waveGrading.js
export function getWaveQuality(windDirection, windSpeed, swellPeriod, beachOrientation, waveHeight) {
    let score = 0;
  
    if (waveHeight < 1) return 'red';
  
    const adjustedWindDirection = (windDirection - beachOrientation + 360) % 360;
    if (adjustedWindDirection >= 240 && adjustedWindDirection <= 300) score += 2;
    if (adjustedWindDirection >= 60 && adjustedWindDirection <= 120) score -= 2;
  
    if (windSpeed <= 5) score += 1;
    else if (windSpeed > 15) score -= 2;
  
    if (swellPeriod >= 10) score += 2;
    if (swellPeriod < 7) score -= 2;
  
    return score >= 4 ? 'green' : score >= 0 ? 'yellow' : 'red';
  }
  