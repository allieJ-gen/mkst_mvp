// 스프레드시트 바운드 스크립트: 관리자 팝업/검색/코멘트 저장

// 스프레드시트 열릴 때 메뉴 추가
function onOpen() {
	SpreadsheetApp.getUi().createMenu('관리자 뷰어').addItem('학생 검색 팝업 열기', 'openAdminViewer').addToUi();
}

// 관리자 팝업 열기
function openAdminViewer() {
	const html = HtmlService.createHtmlOutputFromFile('admin').setWidth(720).setHeight(600);
	SpreadsheetApp.getUi().showModalDialog(html, '관리자 뷰어');
}

// 구성값 반환
function getConfig_() {
	const props = PropertiesService.getScriptProperties();
	return {
		sheetId: props.getProperty('SPREADSHEET_ID'),
		adminEmails: (props.getProperty('ADMIN_EMAILS') || '').split(',').map(s => s.trim()).filter(Boolean),
	};
}

// 관리자 권한 확인
function assertAdmin_() {
	const { adminEmails } = getConfig_();
	const me = Session.getActiveUser().getEmail() || '';
	if (!me || !adminEmails.includes(me)) throw new Error('관리자 권한이 없습니다.');
	return me;
}

// responses 시트 반환
function getResponsesSheet_() {
	const { sheetId } = getConfig_();
	if (!sheetId) throw new Error('SPREADSHEET_ID가 설정되지 않았습니다.');
	const ss = SpreadsheetApp.openById(sheetId);
	const candidates = ['responses', 'ThisCohort'];
	let sh = null;
	for (const name of candidates) { const found = ss.getSheetByName(name); if (found) { sh = found; break; } }
	if (!sh) throw new Error('responses/ThisCohort 시트를 찾을 수 없습니다.');
	return sh;
}

// 이름 검색
function searchByName(name) {
	assertAdmin_();
	const sh = getResponsesSheet_();
	const values = sh.getDataRange().getValues();
	const header = values[0];
	const rows = values.slice(1);
	const idxName = header.indexOf('이름');
	if (idxName < 0) throw new Error('헤더에 이름 컬럼이 없습니다.');
	const matches = [];
	rows.forEach((r, i) => { if (String(r[idxName]).includes(name)) matches.push({ rowIndex: i + 2, data: r }); });
	return { header, matches };
}

// 코멘트 저장(comment_admin)
function saveComment(rowIndex, comment) {
	assertAdmin_();
	const sh = getResponsesSheet_();
	const header = sh.getRange(1,1,1,sh.getLastColumn()).getValues()[0];
	const idx = header.indexOf('comment_admin') + 1;
	if (idx <= 0) throw new Error('comment_admin 컬럼이 없습니다.');
	sh.getRange(rowIndex, idx).setValue(comment || '');
	return { ok: true, rowIndex };
}

// 스크립트 속성 초기화(1회용 실행)
function setupProperties() {
	const props = PropertiesService.getScriptProperties();
	props.setProperties({
		SPREADSHEET_ID: '1GGPlUGBFJp4xn1QWERGlQT1VVwhHtnCj9Z9uUhJ5jg8',
		ADMIN_EMAILS: 'mkst.system@gmail.com,mkst.functional@gmail.com,mkst.submaster@gmail.com,mkst.fmaster@gmail.com'
	}, true);
}


