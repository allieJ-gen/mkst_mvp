// 구성값(SPREADSHEET_ID, ADMIN_EMAILS, RESPONSES_SHEET_NAME) 반환
function getConfig_() {
	// 기본값(fallback) 상수 — 속성 미설정 시에도 동작하도록 함
	const DEFAULT_SHEET_ID = '1GGPlUGBFJp4xn1QWERGlQT1VVwhHtnCj9Z9uUhJ5jg8';
	const DEFAULT_ADMIN_EMAILS = 'mkst.system@gmail.com,mkst.functional@gmail.com,mkst.submaster@gmail.com,mkst.fmaster@gmail.com';
	const DEFAULT_RESPONSES_SHEET = 'responses';
	const props = PropertiesService.getScriptProperties();
	const sheetId = props.getProperty('SPREADSHEET_ID') || DEFAULT_SHEET_ID;
	const emails = (props.getProperty('ADMIN_EMAILS') || DEFAULT_ADMIN_EMAILS)
		.split(',').map(s => s.trim()).filter(Boolean);
	const responsesSheetName = (props.getProperty('RESPONSES_SHEET_NAME') || DEFAULT_RESPONSES_SHEET).trim();
	return { sheetId, adminEmails: emails, responsesSheetName };
}

// responses 시트 핸들 반환(없으면 생성+헤더 보장)
function getResponsesSheet_() {
	const { sheetId, responsesSheetName } = getConfig_();
	if (!sheetId) throw new Error('SPREADSHEET_ID가 설정되지 않았습니다.');
	const ss = SpreadsheetApp.openById(sheetId);
	// 선호 순서대로 탐색: 설정값 → 'responses' → 'ThisCohort'
	const candidates = [responsesSheetName, 'responses', 'ThisCohort']
		.filter((v, i, a) => !!v && a.indexOf(v) === i);
	let sh = null;
	for (const name of candidates) {
		const found = ss.getSheetByName(name);
		if (found) { sh = found; break; }
	}
	if (!sh) sh = ss.insertSheet('responses');
	const headers = [
		'timestamp','respondentId','이름','학교','학년','계열','탐구I','탐구II',
		'주요과목등급','전체평균',
		'국어_내신','수학_내신','영어_내신',
		'국어_모의','수학_모의','영어_모의',
		'탐구I_모의','탐구II_모의',
		'기타과목명_모의','기타_모의',
		'1지망_대학교','2지망_대학교','3지망_대학교',
		'1지망_학과','2지망_학과','3지망_학과',
		'이전공부법','공부법변경이유','김엄마선택이유','김엄마에바라는점',
		'comment_admin','source','version'
	];
	if (sh.getLastRow() === 0) sh.appendRow(headers);
	return sh;
}

// 필수/범위 검증 수행
function validatePayload_(p) {
	const required = ['이름','학교','계열','탐구I','탐구II',
		'주요과목등급','전체평균',
		'국어_내신','수학_내신','영어_내신',
		'국어_모의','수학_모의','영어_모의','탐구I_모의','탐구II_모의',
		'1지망_대학교','2지망_대학교','3지망_대학교','1지망_학과','2지망_학과','3지망_학과',
		'이전공부법','공부법변경이유','김엄마선택이유','김엄마에바라는점'];
	for (const k of required) if (!p[k] && p[k] !== 0) return `${k}은(는) 필수입니다.`;
	const inRange = (v, min, max) => typeof v === 'number' && !isNaN(v) && v >= min && v <= max;
	if (!inRange(p['주요과목등급'], 1, 15)) return '주요과목등급은 1~15 범위여야 합니다.';
	const hundredKeys = ['전체평균','국어_내신','수학_내신','영어_내신','국어_모의','수학_모의','영어_모의','탐구I_모의','탐구II_모의'];
	for (const k of hundredKeys) if (!inRange(p[k], 0, 100)) return `${k}은(는) 0~100 범위여야 합니다.`;
	if (p['기타_모의'] !== undefined && p['기타_모의'] !== '' && !inRange(p['기타_모의'], 0, 100)) return '기타_모의는 0~100 범위여야 합니다.';
	return null;
}

// 설문 제출 처리기(저장)
function submitResponse(payload) {
	const lock = LockService.getScriptLock();
	lock.waitLock(5000);
	try {
		const err = validatePayload_(payload);
		if (err) throw new Error(err);
		const sh = getResponsesSheet_();
		const now = new Date().toISOString();
		const respondentId = payload.respondentId || Utilities.getUuid();
		const row = [
			now, respondentId,
			payload['이름'] || '', payload['학교'] || '', payload['학년'] || '',
			payload['계열'] || '', payload['탐구I'] || '', payload['탐구II'] || '',
			Number(payload['주요과목등급'] || 0), Number(payload['전체평균'] || 0),
			Number(payload['국어_내신'] || 0), Number(payload['수학_내신'] || 0), Number(payload['영어_내신'] || 0),
			Number(payload['국어_모의'] || 0), Number(payload['수학_모의'] || 0), Number(payload['영어_모의'] || 0),
			Number(payload['탐구I_모의'] || 0), Number(payload['탐구II_모의'] || 0),
			payload['기타과목명_모의'] || '', payload['기타_모의'] === '' ? '' : Number(payload['기타_모의']),
			payload['1지망_대학교'] || '', payload['2지망_대학교'] || '', payload['3지망_대학교'] || '',
			payload['1지망_학과'] || '', payload['2지망_학과'] || '', payload['3지망_학과'] || '',
			payload['이전공부법'] || '', payload['공부법변경이유'] || '', payload['김엄마선택이유'] || '', payload['김엄마에바라는점'] || '',
			'', 'webapp', 'v1'
		];
		sh.appendRow(row);
		logAudit_('submit', { ok: true, respondentId });
		return { ok: true, respondentId };
	} catch (e) {
		logAudit_('submit_error', { error: String(e) });
		throw e;
	} finally {
		lock.releaseLock();
	}
}

// 폼 HTML 반환
function doGet(e) {
	return HtmlService.createHtmlOutputFromFile('index').setTitle('김엄마 신입생 상담');
}

// 감사 로깅
function logAudit_(action, payload) {
	const { sheetId } = getConfig_();
	if (!sheetId) return;
	const ss = SpreadsheetApp.openById(sheetId);
	let sh = ss.getSheetByName('audit_log');
	if (!sh) sh = ss.insertSheet('audit_log');
	if (sh.getLastRow() === 0) sh.appendRow(['ts','actor','action','payload']);
	sh.appendRow([new Date().toISOString(), Session.getActiveUser().getEmail() || '', action, JSON.stringify(payload || {})]);
}

// 스크립트 속성 초기화(1회용 실행)
function setupProperties() {
	const props = PropertiesService.getScriptProperties();
	props.setProperties({
		SPREADSHEET_ID: '1GGPlUGBFJp4xn1QWERGlQT1VVwhHtnCj9Z9uUhJ5jg8',
		ADMIN_EMAILS: 'mkst.system@gmail.com,mkst.functional@gmail.com,mkst.submaster@gmail.com,mkst.fmaster@gmail.com'
	}, true);
}


