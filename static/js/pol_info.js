export function getPolInfo(aqi) {
	/**
	 * 根据aqi获取相关信息
	 * return => {aqi, level, color, cond, effect, advice}
	 */
	if(aqi && aqi > 0) {
		if(aqi < 50)
			return { aqi: aqi, level: 1, color: '#73FF73', cond: '优', effect: '空气质量令人满意，基本无空气污染。', advice: '各类人群可正常活动。'};
		else if(aqi < 100)
			return {aqi: aqi, level: 2, color: '#FFFF82', cond: '良', effect: '空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响。', advice: '建议极少数异常敏感人群应减少户外活动。'};
		else if(aqi < 150)
			return {aqi: aqi, level: 3, color: '#FFB973', cond: '轻度污染', effect: '易感人群症状有轻度加剧，健康人群出现刺激症状。', advice: '建议儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼。'};
		else if(aqi < 200)
			return {aqi: aqi, level: 4, color: '#FF7373', cond: '中度污染', effect: '进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响。', advice: '建议疾病患者避免长时间、高强度的户外锻练，一般人群适量减少户外运动。'};
		else if(aqi < 300)
			return {aqi: aqi, level: 5, color: '#AF7373', cond: '重度污染', effect: '心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状。', advice: '建议儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群减少户外运动。'};
		else
			return {aqi: aqi, level: 6, color: '#737373', cond: '严重污染', effect: '健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病。', advice: '建议儿童、老年人和病人应当留在室内，避免体力消耗，一般人群应避免户外活动。'};
	}
}