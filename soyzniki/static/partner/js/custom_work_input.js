
/*
 * Оставь надежду, всяк сюда входящий...
 */

'use strict';

var ID_PREFIX = 'ttwprefix';
var TIME_PATTERN = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$';
var DAY_OF_WEEK = {
	MONDAY    : {short: 'ПН', large: 'Понедельник'},
	TUESDAY   : {short: 'ВТ', large: 'Вторник'},
	WEDNESDAY : {short: 'СР', large: 'Среда'},
	THURSDAY  : {short: 'ЧТ', large: 'Четверг'},
	FRIDAY    : {short: 'ПТ', large: 'Пятница'},
	SATURDAY  : {short: 'СБ', large: 'Суббота'},
	SUNDAY    : {short: 'ВС', large: 'Воскресенье'}
};

$(document).ready( initialize );

function initialize() {

	var hiddenWorkOfTimeClassName = 
		'#id_time_work';
	var workOfTimeList = 
		$(hiddenWorkOfTimeClassName);
	var dayOfWeekModels = [];
	var isFirstFillingFlags = [];
	for (var i=0; i<workOfTimeList.length; i++) {
		var currentHidden = workOfTimeList[i];
		var currentHiddenRawValue = $.trim($(currentHidden).val());
		if ('' == currentHiddenRawValue) {
			var initialRange = '{"ПН":["NONE", "NONE"],' +
				'"ВТ":["NONE", "NONE"],"СР":["NONE", "NONE"],' +
				'"ЧТ":["NONE", "NONE"],"ПТ":["NONE", "NONE"],' +
				'"СБ":["NONE", "NONE"],"ВС":["NONE", "NONE"]}';
			$(currentHidden).val(initialRange);
			currentHiddenRawValue = initialRange;
			isFirstFillingFlags[i] = true;
		} else {
			isFirstFillingFlags[i] = false;
		}
		dayOfWeekModels[i] = JSON.parse(currentHiddenRawValue);
	}

	var radioNameCounter = 0;
	for (var i=0; i<workOfTimeList.length; i++) {

		var currentHidden = workOfTimeList[i];
		var conlrolWrapper = $("<div/>", {
			class : 'custom_work_of_range'
		});
		$(conlrolWrapper).insertAfter(currentHidden);

		var daysButtonWrapper = $("<div/>", {
			class : 'days_button_wrapper'
		});
		$(daysButtonWrapper).appendTo(conlrolWrapper);

		var daysWrapper = $("<div/>", {
			class : 'days_wrapper'
		});
		$(daysWrapper).appendTo(conlrolWrapper);

		var idPreviewWrapper = ID_PREFIX + i + 'daysPreview';
		var previewWrapper = $("<div/>", {
			class : 'days_preview',
			id : idPreviewWrapper
		});
		$(previewWrapper).appendTo(conlrolWrapper);

		for (var day in DAY_OF_WEEK) {
			var isWorkDayModel = 
				(!isNone(dayOfWeekModels[i][DAY_OF_WEEK[day].short][0]));
			var isAroundClockDayModel = 
				('INFINITY' == dayOfWeekModels[i][DAY_OF_WEEK[day].short][0]);
			var isBreaksExistsModel = 
				(dayOfWeekModels[i][DAY_OF_WEEK[day].short].length > 2) ||
				(!isNone(dayOfWeekModels[i][DAY_OF_WEEK[day].short][1]));

			var idDayOfWeek = ID_PREFIX + i + day + 'dayOfWeek';
			var dayofWeek = $("<div/>", {
				class : 'day_of_week',
				id : idDayOfWeek
			});
			$(dayofWeek).appendTo(daysWrapper);

			var dayTab = $("<div/>", {
				class : 'day_tab'
			});
			$(dayTab).appendTo(dayofWeek);

			var tabRow1 = $("<div/>", {
				class : 'tab_row'
			});
			$(tabRow1).appendTo(dayTab);

			var isWorkLabel = $("<label/>", {
				html : 'Рабочий день'
			});
			$(isWorkLabel).appendTo(tabRow1);

			var idIsWorkCheckBox = ID_PREFIX + i + day + 'isWorkCheckBox';
			var isWorkCheckBox = $("<input/>", {
				type : 'checkbox',
				id : idIsWorkCheckBox
			});
			$(isWorkCheckBox).prop('checked', isWorkDayModel);
			$(isWorkLabel).prepend(isWorkCheckBox);

			var tabRow2 = $("<div/>", {
				class : 'tab_row'
			});
			$(tabRow2).appendTo(dayTab);

			var aroundClockLabel = $("<label/>", {
				html : 'Круглосуточно'
			});
			$(aroundClockLabel).appendTo(tabRow2);

			var radioModeName = 
				'modeRadio' + radioNameCounter++;
			var idModeRadio1 = ID_PREFIX + i + day + 'modeRadio1';
			var modeRadio1 = $("<input/>", {
				type : 'radio',
				name : radioModeName,
				id : idModeRadio1
			});
			if (isWorkDayModel) {
				$(modeRadio1).prop('checked', isAroundClockDayModel);
			}
			$(aroundClockLabel).prepend(modeRadio1);

			var tabRow3 = $("<div/>", {
				class : 'tab_row'
			});
			$(tabRow3).appendTo(dayTab);

			var workingRangeLabel = $("<label/>", {
			});
			$(workingRangeLabel).appendTo(tabRow3);

			var idModeRadio2 = ID_PREFIX + i + day + 'modeRadio2';
			var modeRadio2 = $("<input/>", {
				type : 'radio',
				name : radioModeName,
				id : idModeRadio2
			});
			if (isWorkDayModel) {
				$(modeRadio2).prop('checked', !isAroundClockDayModel);
			}
			$(workingRangeLabel).prepend(modeRadio2);

			var rangeSpanPart1 = $("<span/>", {
				html : 'С '
			});
			$(rangeSpanPart1).appendTo(workingRangeLabel);

			var idRangeInputFrom = ID_PREFIX + i + day + 'rangeInputFrom';
			var fromVal = (isWorkDayModel && !isAroundClockDayModel) 
				? dayOfWeekModels[i][DAY_OF_WEEK[day].short][0][0] : '';
			var rangeInputFrom = $("<input/>", {
				type : 'text',
				name : 'from',
				value : fromVal,
				id : idRangeInputFrom,
				pattern : TIME_PATTERN,
				placeholder : '00:00'
			});
			$(rangeInputFrom).appendTo(workingRangeLabel);

			$(rangeInputFrom).focus({ i: i, day: day }, 
					function(event) {
				var reqModeRadio = '#' + ID_PREFIX + event.data.i 
					+ event.data.day + 'modeRadio2';
				$(reqModeRadio).prop("checked", true);
			});

			$(rangeInputFrom).blur({ i: i, day: day }, 
					function(event) {

				
				var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').val();
				var bufToValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').val();

				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
				if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						[bufFromValue,bufToValue];
				} else {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						'INFINITY';
				}

				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var breakRows = 
					$(containerId + ' .breaks_container_row');
				var counter = 1;
				for (var k=0; k<breakRows.length; k++) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][counter] =
							[$(breakRows[k])
								.find('input[name=from]')
								.val(),
							$(breakRows[k])
								.find('input[name=to]')
								.val()];
					counter++;
				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);

				var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml);
			});

			var rangeSpanPart2 = $("<span/>", {
				html : ' по '
			});
			$(rangeSpanPart2).appendTo(workingRangeLabel);

			var idRangeInputTo = ID_PREFIX + i + day + 'rangeInputTo';
			var toVal = (isWorkDayModel && !isAroundClockDayModel) 
				? dayOfWeekModels[i][DAY_OF_WEEK[day].short][0][1] : '';
			var rangeInputTo = $("<input/>", {
				type : 'text',
				name : 'to',
				value : toVal,
				id : idRangeInputTo,
				placeholder : '00:00'
			});
			$(rangeInputTo).appendTo(workingRangeLabel);

			$(rangeInputTo).focus({ i: i, day: day }, 
					function(event) {
				var reqModeRadio = '#' + ID_PREFIX + event.data.i 
					+ event.data.day + 'modeRadio2';
				$(reqModeRadio).prop("checked", true);
			});

			$(rangeInputTo).blur({ i: i, day: day }, 
					function(event) {

				var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').val();
				var bufToValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').val();

				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
				if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						[bufFromValue,bufToValue];
				} else {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						'INFINITY';
				}

				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var breakRows = 
					$(containerId + ' .breaks_container_row');
				var counter = 1;
				for (var k=0; k<breakRows.length; k++) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][counter] =
							[$(breakRows[k])
								.find('input[name=from]')
								.val(),
							$(breakRows[k])
								.find('input[name=to]')
								.val()];
					counter++;
				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);
				var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml); 
			});

			var idBreaksContainer = ID_PREFIX + i + day + 'breaksContainer';
			var breaksContainer = $("<div/>", {
				class : 'breaks_container',
				id : idBreaksContainer
			});
			$(breaksContainer).appendTo(dayTab);

			if (isBreaksExistsModel) {
				for (var j=1; j<dayOfWeekModels[i][DAY_OF_WEEK[day].short].length;
					j++) {
					var breaksContainerRow = $("<div/>", {
						class : 'breaks_container_row'
					});
					$(breaksContainerRow).appendTo(breaksContainer);

					var breakRangeLabel = $("<label/>", {
					});
					$(breakRangeLabel).appendTo(breaksContainerRow);

					var breakRangeSpanPart1 = $("<span/>", {
						html : 'Перерыв с '
					});
					$(breakRangeSpanPart1).appendTo(breakRangeLabel);

					var breakFromVal = dayOfWeekModels[i]
							[DAY_OF_WEEK[day].short][j][0];
					var breakRangeInputFrom = $("<input/>", {
						type : 'text',
						name : 'from',
						value : breakFromVal,
						pattern : TIME_PATTERN,
						placeholder : '00:00'
					});
					$(breakRangeInputFrom).appendTo(breakRangeLabel);

					$(breakRangeInputFrom).blur({ i: i, day: day }, 
							function(event) {

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}
						

						var containerPrefix = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId = containerPrefix + 'breaksContainer';
						var breakRows = 
							$(containerId + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});

					var breakRangeSpanPart2 = $("<span/>", {
						html : ' по '
					});
					$(breakRangeSpanPart2).appendTo(breakRangeLabel);

					var breakToVal = dayOfWeekModels[i]
							[DAY_OF_WEEK[day].short][j][1];
					var breakRangeInputTo = $("<input/>", {
						type : 'text',
						name : 'to',
						value : breakToVal,
						pattern : TIME_PATTERN,
						placeholder : '00:00'
					});
					$(breakRangeInputTo).appendTo(breakRangeLabel);

					$(breakRangeInputTo).blur({ i: i, day: day }, 
							function(event) {

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}

						var containerPrefix = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId = containerPrefix + 'breaksContainer';
						var breakRows = 
							$(containerId + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});

					var breakDeleteButton = $("<button/>", {
						class : 'delete_break_button',
						html : '&#10006;'
					});
					$(breakDeleteButton).appendTo(breaksContainerRow);

					$(breakDeleteButton).on("click", { i: i, day: day }, function(event) {
						event.preventDefault ? event.preventDefault() : (event.returnValue = false);
						var containerId = '#' + ID_PREFIX + event.data.i 
							+ event.data.day + 'breaksContainer';
						var existCount = $(containerId + ' .breaks_container_row').length;
						if (existCount == 3) {
							var addBreakButtonId = '#' + ID_PREFIX + event.data.i 
								+ event.data.day + 'addBreakButton';
							$(addBreakButtonId).show();
						}
						$(this).parent('.breaks_container_row').remove();

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}

						var containerPrefix2 = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId2 = containerPrefix2 + 'breaksContainer';
						var breakRows = 
							$(containerId2 + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});
				}
			}

			var tabRow4 = $("<div/>", {
				class : 'tab_row'
			});
			$(tabRow4).appendTo(dayTab);

			var idAddBreakButton = 
				ID_PREFIX + i + day + 'addBreakButton';
			var addBreakButton = $("<button/>", {
				class : 'add_break_button big_button',
				html : 'Добавить перерыв',
				id : idAddBreakButton
			});
			$(addBreakButton).appendTo(tabRow4);
			if (dayOfWeekModels[i][DAY_OF_WEEK[day].short].length >= 3) {
				$(addBreakButton).hide();
			}

			// Изменение чекбокса "Рабочий день"
			$(isWorkCheckBox).change({ i: i, day: day }, function(event) {
				if (this.checked) { // если включаем рабочий
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short] = 
							['INFINITY',"NONE"];
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio1').prop('checked', true);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio1').prop('disabled', false);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio2').prop('disabled', false);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').prop('disabled', false);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').prop('disabled', false);
					var containerPrefix = '#' + ID_PREFIX + event.data.i 
						+ event.data.day;
					$(containerPrefix + 'addBreakButton').show();	

				} else {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio1').prop('checked', false);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio2').prop('checked', false);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio1').prop('disabled', true);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'modeRadio2').prop('disabled', true);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').prop('disabled', true);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').prop('disabled', true);
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').val('');
					$('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').val('');
					var containerPrefix = '#' + ID_PREFIX + event.data.i 
						+ event.data.day;
					$(containerPrefix + 'breaksContainer .breaks_container_row').remove();
					$(containerPrefix + 'addBreakButton').hide();

				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);
				var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml); 
			});


			$(addBreakButton).on("click", { i: i, day: day }, 
					function(event) {
				event.preventDefault ? event.preventDefault() : (event.returnValue = false);
				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var existCount = $(containerId + ' .breaks_container_row').length;
				if (existCount < 3) {

					var breaksContainerRow = $("<div/>", {
						class : 'breaks_container_row'
					});
					$(breaksContainerRow).appendTo(containerId);

					var breakRangeLabel = $("<label/>", {
					});
					$(breakRangeLabel).appendTo(breaksContainerRow);

					var breakRangeSpanPart1 = $("<span/>", {
						html : 'Перерыв с '
					});
					$(breakRangeSpanPart1).appendTo(breakRangeLabel);

					var breakRangeInputFrom = $("<input/>", {
						type : 'text',
						name : 'from',
						pattern : TIME_PATTERN,
						placeholder : '00:00'
					});
					$(breakRangeInputFrom).appendTo(breakRangeLabel);

					$(breakRangeInputFrom).blur(
							{ i: event.data.i, day: event.data.day }, 
							function(event) {

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}

						var containerPrefix = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId2 = containerPrefix + 'breaksContainer';
						var breakRows = 
							$(containerId2 + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});

					var breakRangeSpanPart2 = $("<span/>", {
						html : ' по '
					});
					$(breakRangeSpanPart2).appendTo(breakRangeLabel);

					var breakRangeInputTo = $("<input/>", {
						type : 'text',
						name : 'to',
						pattern : TIME_PATTERN,
						placeholder : '00:00'
					});
					$(breakRangeInputTo).appendTo(breakRangeLabel);

					$(breakRangeInputTo).blur(
							{ i: event.data.i, day: event.data.day }, 
							function(event) {

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}

						var containerPrefix = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId = containerPrefix + 'breaksContainer';
						var breakRows = 
							$(containerId + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});

					var breakDeleteButton = $("<button/>", {
						class : 'delete_break_button',
						html : '&#10006;'
					});
					$(breakDeleteButton).appendTo(breaksContainerRow);

					$(breakDeleteButton).on("click", {containerPrefix: containerPrefix, i: event.data.i, day: event.data.day }, 
							function(event) {
						event.preventDefault ? event.preventDefault() : (event.returnValue = false);
						var containerId = containerPrefix + 'breaksContainer';
						var existCount = 
							$(containerId + ' .breaks_container_row').length;
						if (existCount == 3) {

							var addBreakButtonId = containerPrefix + 'addBreakButton';
							$(addBreakButtonId).show();
						}
						$(this).parent('.breaks_container_row')
							.remove();

						var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputFrom').val();
						var bufToValue = $('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'rangeInputTo').val();

						dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
						if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								[bufFromValue,bufToValue];
						} else {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][0] =
								'INFINITY';
						}

						var containerPrefix2 = '#' + ID_PREFIX + event.data.i 
							+ event.data.day;
						var containerId2 = containerPrefix2 + 'breaksContainer';
						var breakRows = 
							$(containerId2 + ' .breaks_container_row');
						var counter = 1;
						for (var k=0; k<breakRows.length; k++) {
							dayOfWeekModels[event.data.i]
								[DAY_OF_WEEK[event.data.day].short][counter] =
									[$(breakRows[k])
										.find('input[name=from]')
										.val(),
									$(breakRows[k])
										.find('input[name=to]')
										.val()];
							counter++;
						}
						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);
						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					});

				}
				if (existCount == 2) {
					$(this).hide();
				}

				var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').val();
				var bufToValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').val();

				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
				if ($('#' + ID_PREFIX + event.data.i + 
								event.data.day + 'modeRadio2').prop('checked')) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						[bufFromValue,bufToValue];
				} else {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][0] =
						'INFINITY';
				}

				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var breakRows = 
					$(containerId + ' .breaks_container_row');
				var counter = 1;
				for (var k=0; k<breakRows.length; k++) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][counter] =
							[$(breakRows[k])
								.find('input[name=from]')
								.val(),
							$(breakRows[k])
								.find('input[name=to]')
								.val()];
					counter++;
				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);
									var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml); 
			
			});

			// Клик по радио "Круглосуточно"
			$(modeRadio1).change({ i: i, day: day }, function(event) {

				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short][0] =
						'INFINITY';

				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var breakRows = 
					$(containerId + ' .breaks_container_row');
				var counter = 1;
				for (var k=0; k<breakRows.length; k++) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][counter] =
							[$(breakRows[k])
								.find('input[name=from]')
								.val(),
							$(breakRows[k])
								.find('input[name=to]')
								.val()];
					counter++;
				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);
				var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml); 
			});

			// Клик по радио "C/по"
			$(modeRadio2).change({ i: i, day: day }, function(event) {

				var fromValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputFrom').val();
				var toValue = $('#' + ID_PREFIX + event.data.i + 
						event.data.day + 'rangeInputTo').val();

				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
				dayOfWeekModels[event.data.i]
					[DAY_OF_WEEK[event.data.day].short][0] =
						[fromValue,toValue];

				var containerPrefix = '#' + ID_PREFIX + event.data.i 
					+ event.data.day;
				var containerId = containerPrefix + 'breaksContainer';
				var breakRows = 
					$(containerId + ' .breaks_container_row');
				var counter = 1;
				for (var k=0; k<breakRows.length; k++) {
					dayOfWeekModels[event.data.i]
						[DAY_OF_WEEK[event.data.day].short][counter] =
							[$(breakRows[k])
								.find('input[name=from]')
								.val(),
							$(breakRows[k])
								.find('input[name=to]')
								.val()];
					counter++;
				}
				$(workOfTimeList[event.data.i]).val(
					JSON.stringify(dayOfWeekModels[event.data.i])
				);
				var errorMessage = '';
				var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
				var rawHtml = '';
				for (var outDay in DAY_OF_WEEK) {
					rawHtml += '<span class="preview_row">'
					var wt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][0];
					rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
						+ '</b>';
					rawHtml += ': ';

					if ('INFINITY' == wt) {
						rawHtml += 'Круглосуточно';
					} else if (isNone(wt)) {
						rawHtml += 'Не работает';
					} else {
						var isValid = true;
						isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
						isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
						if (!isValid) {
							rawHtml += '<span style="color: red;">'
						}
						rawHtml += wt[0] + ' - ' + wt[1];
						if (!isValid) {
							rawHtml += '</span>';
							if (errorMessage != '') {
								errorMessage += '<br>';
							}
							errorMessage += 'Ошибка ввода: ' + 
								DAY_OF_WEEK[outDay].large;
						}
					}
					rawHtml += '</span><br>';
					if (isNone(wt)) {
						continue;
					}
					for (var bi=1; bi < dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length; bi++) {
						rawHtml += '<span class="preview_row">'
						var bt = dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short][bi];
						if (bt == "NONE") {
							rawHtml += 'Без перерывов';
						} else {
							var isValid = true;
							isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
							isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
							if (!isValid) {
								rawHtml += '<span style="color: red;">'
							}
							rawHtml += '(перерыв): ' 
								+ bt[0] + ' - ' + bt[1];
							if (!isValid) {
								rawHtml += '</span>';
								if (errorMessage != '') {
									errorMessage += '<br>';
								}
								errorMessage += 'Ошибка ввода: ' + 
									DAY_OF_WEEK[outDay].large;
							}
						}
						rawHtml += '</span>';
						if ((bi+1 != dayOfWeekModels[event.data.i]
							[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
							rawHtml += '<br>';
						}
					}
				}
				if (errorMessage != '') {
					rawHtml = '<span style="color: red;" class="preview_row">'
						+ errorMessage + '</span><br>' + rawHtml;
				}
				$(idPreviewWrapper).html(rawHtml); 
			});

			if (!isWorkDayModel) {
				$('#' + ID_PREFIX + i + 
					day + 'modeRadio1').prop('checked', false);
				$('#' + ID_PREFIX + i + 
					day + 'modeRadio2').prop('checked', false);
				$('#' + ID_PREFIX + i + 
					day + 'modeRadio1').prop('disabled', true);
				$('#' + ID_PREFIX + i + 
					day + 'modeRadio2').prop('disabled', true);
				$('#' + ID_PREFIX + i + 
					day + 'rangeInputFrom').prop('disabled', true);
				$('#' + ID_PREFIX + i + 
					day + 'rangeInputTo').prop('disabled', true);
				$('#' + ID_PREFIX + i + 
					day + 'rangeInputFrom').val('');
				$('#' + ID_PREFIX + i + 
					day + 'rangeInputTo').val('');
				var containerPrefix = '#' + ID_PREFIX + i 
					+ day;
				$(containerPrefix + 'breaksContainer .breaks_container_row').remove();
				$(containerPrefix + 'addBreakButton').hide();
			}

		}

		for (var day in DAY_OF_WEEK) {
			
			var dayButton = $("<button/>", {
				class : 'day_button',
				html : DAY_OF_WEEK[day].short
			});
			$(dayButton).appendTo(daysButtonWrapper);

			$(dayButton).on("click", { i: i, day: day }, function(event) {
				event.preventDefault ? event.preventDefault() : (event.returnValue = false);
				var idDayOfWeek = '#' + ID_PREFIX + event.data.i 
					+ event.data.day + 'dayOfWeek';
				$(this).parent().parent().find('.day_of_week').hide();
				$(idDayOfWeek).show();

				$(this).parent().find('.day_button').removeClass('active');
				$(this).addClass('active');

				if (isFirstFillingFlags[event.data.i]) {
					var checkeds = $(this).parent().parent()
						.find('input[type="checkbox"]:checked');
					if (checkeds.length != 0) {
						isFirstFillingFlags[event.data.i] = false;
						var chekedDay = checkeds[0].id.substring(
							(ID_PREFIX + event.data.i).length, 
							checkeds[0].id.length 
								- 'isWorkCheckBox'.length);
						var checkedIsAroundClock = $('#' + ID_PREFIX + event.data.i 
							+ chekedDay + 'modeRadio1').prop('checked');
						var checkedIsWorkRange = $('#' + ID_PREFIX + event.data.i 
							+ chekedDay + 'modeRadio2').prop('checked');
						if (checkedIsAroundClock) {
							for (var current in DAY_OF_WEEK) {
								dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[current].short][0] 
										= 'INFINITY';
								$('#' + ID_PREFIX + event.data.i 
									+ current + 'isWorkCheckBox')
									.prop('checked', true);
								$('#' + ID_PREFIX + event.data.i 
									+ current + 'modeRadio1')
									.prop('checked', true);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'modeRadio1').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'modeRadio2').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'rangeInputFrom').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'rangeInputTo').prop('disabled', false);

								if (current != chekedDay) {
									var firstBreak = dayOfWeekModels[event.data.i]
										[DAY_OF_WEEK[chekedDay].short][1];
									if (!isNone(firstBreak)) {
										var countBreaks = dayOfWeekModels[event.data.i]
											[DAY_OF_WEEK[chekedDay].short].length-1;
										for (var rr=0; rr<countBreaks; rr++) {
											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[current].short][rr+1] = 
											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[chekedDay].short][rr+1];
										}
									}
								}
							}
						} else if (checkedIsWorkRange) {
							var checkedFromValue = $('#' + ID_PREFIX + event.data.i + 
									chekedDay + 'rangeInputFrom').val();
							var checkedToValue = $('#' + ID_PREFIX + event.data.i + 
									chekedDay + 'rangeInputTo').val();
							
							for (var current in DAY_OF_WEEK) {
								dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[current].short][0] 
										= [checkedFromValue, checkedToValue];
								$('#' + ID_PREFIX + event.data.i 
									+ current + 'isWorkCheckBox')
									.prop('checked', true);
								$('#' + ID_PREFIX + event.data.i 
									+ current + 'modeRadio2')
									.prop('checked', true);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'modeRadio1').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'modeRadio2').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'rangeInputFrom').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + 
									current + 'rangeInputTo').prop('disabled', false);
								$('#' + ID_PREFIX + event.data.i + current 
									+ 'rangeInputFrom').val(checkedFromValue);
								$('#' + ID_PREFIX + event.data.i + current 
									+ 'rangeInputTo').val(checkedToValue);

								if (current != chekedDay) {
									var firstBreak = dayOfWeekModels[event.data.i]
										[DAY_OF_WEEK[chekedDay].short][1];
									if (!isNone(firstBreak)) {
										var countBreaks = dayOfWeekModels[event.data.i]
											[DAY_OF_WEEK[chekedDay].short].length-1;
										for (var rr=0; rr<countBreaks; rr++) {
											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[current].short][rr+1] = 
											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[chekedDay].short][rr+1];
										}
									}
								}
							}
						} else {
							console.log('Error state algoritm.');
							return;
						}

						$(workOfTimeList[event.data.i]).val(
							JSON.stringify(dayOfWeekModels[event.data.i])
						);

						for (var current in DAY_OF_WEEK) {
							if (current != chekedDay) {
								var firstBreak = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[chekedDay].short][1];
								if (!isNone(firstBreak)) {
									for (var rr=0; rr<countBreaks; rr++) {
										var fromV = dayOfWeekModels[event.data.i][DAY_OF_WEEK[current].short][rr+1][0];
										var toV = dayOfWeekModels[event.data.i][DAY_OF_WEEK[current].short][rr+1][1];

										var breaksContainerRow = $("<div/>", {
											class : 'breaks_container_row'
										});
										$(breaksContainerRow).appendTo('#' + ID_PREFIX 
											+ event.data.i + current + 'breaksContainer');

										var breakRangeLabel = $("<label/>", {
										});
										$(breakRangeLabel).appendTo(breaksContainerRow);

										var breakRangeSpanPart1 = $("<span/>", {
											html : 'Перерыв с '
										});
										$(breakRangeSpanPart1).appendTo(breakRangeLabel);

										var breakRangeInputFrom = $("<input/>", {
											type : 'text',
											name : 'from',
											value : fromV,
											pattern : TIME_PATTERN,
											placeholder : '00:00'
										});
										$(breakRangeInputFrom).appendTo(breakRangeLabel);

										$(breakRangeInputFrom).blur({ i: event.data.i, day: current }, 
												function(event) {

											var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputFrom').val();
											var bufToValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputTo').val();

											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
											if ($('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'modeRadio2').prop('checked')) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													[bufFromValue,bufToValue];
											} else {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													'INFINITY';
											}
											

											var containerPrefix = '#' + ID_PREFIX + event.data.i 
												+ event.data.day;
											var containerId = containerPrefix + 'breaksContainer';
											var breakRows = 
												$(containerId + ' .breaks_container_row');
											var counter = 1;
											for (var k2=0; k2<breakRows.length; k2++) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][counter] =
														[$(breakRows[k2])
															.find('input[name=from]')
															.val(),
														$(breakRows[k2])
															.find('input[name=to]')
															.val()];
												counter++;
											}
											$(workOfTimeList[event.data.i]).val(
												JSON.stringify(dayOfWeekModels[event.data.i])
											);
											var errorMessage = '';
											var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
											var rawHtml = '';
											for (var outDay in DAY_OF_WEEK) {
												rawHtml += '<span class="preview_row">'
												var wt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][0];
												rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
													+ '</b>';
												rawHtml += ': ';

												if ('INFINITY' == wt) {
													rawHtml += 'Круглосуточно';
												} else if (isNone(wt)) {
													rawHtml += 'Не работает';
												} else {
													var isValid = true;
													isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
													isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
													if (!isValid) {
														rawHtml += '<span style="color: red;">'
													}
													rawHtml += wt[0] + ' - ' + wt[1];
													if (!isValid) {
														rawHtml += '</span>';
														if (errorMessage != '') {
															errorMessage += '<br>';
														}
														errorMessage += 'Ошибка ввода: ' + 
															DAY_OF_WEEK[outDay].large;
													}
												}
												rawHtml += '</span><br>';
												if (isNone(wt)) {
													continue;
												}
												for (var bi=1; bi < dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length; bi++) {
													rawHtml += '<span class="preview_row">'
													var bt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][bi];
													if (bt == "NONE") {
														rawHtml += 'Без перерывов';
													} else {
														var isValid = true;
														isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
														isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
														if (!isValid) {
															rawHtml += '<span style="color: red;">'
														}
														rawHtml += '(перерыв): ' 
															+ bt[0] + ' - ' + bt[1];
														if (!isValid) {
															rawHtml += '</span>';
															if (errorMessage != '') {
																errorMessage += '<br>';
															}
															errorMessage += 'Ошибка ввода: ' + 
																DAY_OF_WEEK[outDay].large;
														}
													}
													rawHtml += '</span>';
													if ((bi+1 != dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
														rawHtml += '<br>';
													}
												}
											}
											if (errorMessage != '') {
												rawHtml = '<span style="color: red;" class="preview_row">'
													+ errorMessage + '</span><br>' + rawHtml;
											}
											$(idPreviewWrapper).html(rawHtml); 
										});

										var breakRangeSpanPart2 = $("<span/>", {
											html : ' по '
										});
										$(breakRangeSpanPart2).appendTo(breakRangeLabel);

										var breakRangeInputTo = $("<input/>", {
											type : 'text',
											name : 'to',
											value : toV,
											pattern : TIME_PATTERN,
											placeholder : '00:00'
										});
										$(breakRangeInputTo).appendTo(breakRangeLabel);

										$(breakRangeInputTo).blur({ i: event.data.i, day: current }, 
												function(event) {

											var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputFrom').val();
											var bufToValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputTo').val();

											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
											if ($('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'modeRadio2').prop('checked')) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													[bufFromValue,bufToValue];
											} else {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													'INFINITY';
											}

											var containerPrefix = '#' + ID_PREFIX + event.data.i 
												+ event.data.day;
											var containerId = containerPrefix + 'breaksContainer';
											var breakRows = 
												$(containerId + ' .breaks_container_row');
											var counter = 1;
											for (var k4=0; k4<breakRows.length; k4++) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][counter] =
														[$(breakRows[k4])
															.find('input[name=from]')
															.val(),
														$(breakRows[k4])
															.find('input[name=to]')
															.val()];
												counter++;
											}
											$(workOfTimeList[event.data.i]).val(
												JSON.stringify(dayOfWeekModels[event.data.i])
											);
											var errorMessage = '';
											var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
											var rawHtml = '';
											for (var outDay in DAY_OF_WEEK) {
												rawHtml += '<span class="preview_row">'
												var wt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][0];
												rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
													+ '</b>';
												rawHtml += ': ';

												if ('INFINITY' == wt) {
													rawHtml += 'Круглосуточно';
												} else if (isNone(wt)) {
													rawHtml += 'Не работает';
												} else {
													var isValid = true;
													isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
													isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
													if (!isValid) {
														rawHtml += '<span style="color: red;">'
													}
													rawHtml += wt[0] + ' - ' + wt[1];
													if (!isValid) {
														rawHtml += '</span>';
														if (errorMessage != '') {
															errorMessage += '<br>';
														}
														errorMessage += 'Ошибка ввода: ' + 
															DAY_OF_WEEK[outDay].large;
													}
												}
												rawHtml += '</span><br>';
												if (isNone(wt)) {
													continue;
												}
												for (var bi=1; bi < dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length; bi++) {
													rawHtml += '<span class="preview_row">'
													var bt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][bi];
													if (bt == "NONE") {
														rawHtml += 'Без перерывов';
													} else {
														var isValid = true;
														isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
														isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
														if (!isValid) {
															rawHtml += '<span style="color: red;">'
														}
														rawHtml += '(перерыв): ' 
															+ bt[0] + ' - ' + bt[1];
														if (!isValid) {
															rawHtml += '</span>';
															if (errorMessage != '') {
																errorMessage += '<br>';
															}
															errorMessage += 'Ошибка ввода: ' + 
																DAY_OF_WEEK[outDay].large;
														}
													}
													rawHtml += '</span>';
													if ((bi+1 != dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
														rawHtml += '<br>';
													}
												}
											}
											if (errorMessage != '') {
												rawHtml = '<span style="color: red;" class="preview_row">'
													+ errorMessage + '</span><br>' + rawHtml;
											}
											$(idPreviewWrapper).html(rawHtml); 
										});

										var breakDeleteButton = $("<button/>", {
											class : 'delete_break_button',
											html : '&#10006;'
										});
										$(breakDeleteButton).appendTo(breaksContainerRow);

										$(breakDeleteButton).on("click", { i: event.data.i, day: current }, function(event) {
											event.preventDefault ? event.preventDefault() : (event.returnValue = false);
											var containerId = '#' + ID_PREFIX + event.data.i 
												+ event.data.day + 'breaksContainer';
											var existCount = $(containerId + ' .breaks_container_row').length;
											if (existCount == 3) {
												var addBreakButtonId = '#' + ID_PREFIX + event.data.i 
													+ event.data.day + 'addBreakButton';
												$(addBreakButtonId).show();
											}
											$(this).parent('.breaks_container_row').remove();

											var bufFromValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputFrom').val();
											var bufToValue = $('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'rangeInputTo').val();

											dayOfWeekModels[event.data.i]
												[DAY_OF_WEEK[event.data.day].short] = ["NONE","NONE"];
											if ($('#' + ID_PREFIX + event.data.i + 
													event.data.day + 'modeRadio2').prop('checked')) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													[bufFromValue,bufToValue];
											} else {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][0] =
													'INFINITY';
											}

											var containerPrefix2 = '#' + ID_PREFIX + event.data.i 
												+ event.data.day;
											var containerId2 = containerPrefix2 + 'breaksContainer';
											var breakRows = 
												$(containerId2 + ' .breaks_container_row');
											var counter = 1;
											for (var k=0; k<breakRows.length; k++) {
												dayOfWeekModels[event.data.i]
													[DAY_OF_WEEK[event.data.day].short][counter] =
														[$(breakRows[k])
															.find('input[name=from]')
															.val(),
														$(breakRows[k])
															.find('input[name=to]')
															.val()];
												counter++;
											}
											$(workOfTimeList[event.data.i]).val(
												JSON.stringify(dayOfWeekModels[event.data.i])
											);
											var errorMessage = '';
											var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
											var rawHtml = '';
											for (var outDay in DAY_OF_WEEK) {
												rawHtml += '<span class="preview_row">'
												var wt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][0];
												rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
													+ '</b>';
												rawHtml += ': ';

												if ('INFINITY' == wt) {
													rawHtml += 'Круглосуточно';
												} else if (isNone(wt)) {
													rawHtml += 'Не работает';
												} else {
													var isValid = true;
													isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
													isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
													if (!isValid) {
														rawHtml += '<span style="color: red;">'
													}
													rawHtml += wt[0] + ' - ' + wt[1];
													if (!isValid) {
														rawHtml += '</span>';
														if (errorMessage != '') {
															errorMessage += '<br>';
														}
														errorMessage += 'Ошибка ввода: ' + 
															DAY_OF_WEEK[outDay].large;
													}
												}
												rawHtml += '</span><br>';
												if (isNone(wt)) {
													continue;
												}
												for (var bi=1; bi < dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length; bi++) {
													rawHtml += '<span class="preview_row">'
													var bt = dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short][bi];
													if (bt == "NONE") {
														rawHtml += 'Без перерывов';
													} else {
														var isValid = true;
														isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
														isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
														if (!isValid) {
															rawHtml += '<span style="color: red;">'
														}
														rawHtml += '(перерыв): ' 
															+ bt[0] + ' - ' + bt[1];
														if (!isValid) {
															rawHtml += '</span>';
															if (errorMessage != '') {
																errorMessage += '<br>';
															}
															errorMessage += 'Ошибка ввода: ' + 
																DAY_OF_WEEK[outDay].large;
														}
													}
													rawHtml += '</span>';
													if ((bi+1 != dayOfWeekModels[event.data.i]
														[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
														rawHtml += '<br>';
													}
												}
											}
											if (errorMessage != '') {
												rawHtml = '<span style="color: red;" class="preview_row">'
													+ errorMessage + '</span><br>' + rawHtml;
											}
											$(idPreviewWrapper).html(rawHtml); 
										});

									}
								}
								var addBreakButtonId = '#' + ID_PREFIX + event.data.i + current + 'addBreakButton';	
								if (dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[chekedDay].short].length <= 3) {
									$(addBreakButtonId).show();
								} else {
									$(addBreakButtonId).hide();
								}
							}
						}

						var errorMessage = '';
						var idPreviewWrapper = '#' + ID_PREFIX + event.data.i + 'daysPreview';
						var rawHtml = '';
						for (var outDay in DAY_OF_WEEK) {
							rawHtml += '<span class="preview_row">'
							var wt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][0];
							rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
								+ '</b>';
							rawHtml += ': ';

							if ('INFINITY' == wt) {
								rawHtml += 'Круглосуточно';
							} else if (isNone(wt)) {
								rawHtml += 'Не работает';
							} else {
								var isValid = true;
								isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
								isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
								if (!isValid) {
									rawHtml += '<span style="color: red;">'
								}
								rawHtml += wt[0] + ' - ' + wt[1];
								if (!isValid) {
									rawHtml += '</span>';
									if (errorMessage != '') {
										errorMessage += '<br>';
									}
									errorMessage += 'Ошибка ввода: ' + 
										DAY_OF_WEEK[outDay].large;
								}
							}
							rawHtml += '</span><br>';
							if (isNone(wt)) {
								continue;
							}
							for (var bi=1; bi < dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length; bi++) {
								rawHtml += '<span class="preview_row">'
								var bt = dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short][bi];
								if (bt == "NONE") {
									rawHtml += 'Без перерывов';
								} else {
									var isValid = true;
									isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
									isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
									if (!isValid) {
										rawHtml += '<span style="color: red;">'
									}
									rawHtml += '(перерыв): ' 
										+ bt[0] + ' - ' + bt[1];
									if (!isValid) {
										rawHtml += '</span>';
										if (errorMessage != '') {
											errorMessage += '<br>';
										}
										errorMessage += 'Ошибка ввода: ' + 
											DAY_OF_WEEK[outDay].large;
									}
								}
								rawHtml += '</span>';
								if ((bi+1 != dayOfWeekModels[event.data.i]
									[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
									rawHtml += '<br>';
								}
							}
						}
						if (errorMessage != '') {
							rawHtml = '<span style="color: red;" class="preview_row">'
								+ errorMessage + '</span><br>' + rawHtml;
						}
						$(idPreviewWrapper).html(rawHtml); 
					}
				}
			});
		}

		$(daysButtonWrapper).find('.day_button').first().addClass('active');

		$(daysWrapper).find('.day_of_week').hide();
		$(daysWrapper).find('.day_of_week').first().show();

		var errorMessage = '';
		var idPreviewWrapper = '#' + ID_PREFIX + i + 'daysPreview';
		var rawHtml = '';
		for (var outDay in DAY_OF_WEEK) {
			rawHtml += '<span class="preview_row">'
			var wt = dayOfWeekModels[i]
					[DAY_OF_WEEK[outDay].short][0];
			rawHtml += '<b>' + DAY_OF_WEEK[outDay].short 
				+ '</b>';
			rawHtml += ': ';

			if ('INFINITY' == wt) {
				rawHtml += 'Круглосуточно';
			} else if (isNone(wt)) {
				rawHtml += 'Не работает';
			} else {
				var isValid = true;
				isValid &= (new RegExp(TIME_PATTERN).test(wt[0]));
				isValid &= (new RegExp(TIME_PATTERN).test(wt[1])); 
				if (!isValid) {
					rawHtml += '<span style="color: red;">'
				}
				rawHtml += wt[0] + ' - ' + wt[1];
				if (!isValid) {
					rawHtml += '</span>';
					if (errorMessage != '') {
						errorMessage += '<br>';
					}
					errorMessage += 'Ошибка ввода: ' + 
						DAY_OF_WEEK[outDay].large;
				}
			}
			rawHtml += '</span><br>';
			if (isNone(wt)) {
				continue;
			}
			for (var bi=1; bi < dayOfWeekModels[i]
					[DAY_OF_WEEK[outDay].short].length; bi++) {
				rawHtml += '<span class="preview_row">'
				var bt = dayOfWeekModels[i]
					[DAY_OF_WEEK[outDay].short][bi];
				if (bt == "NONE") {
					rawHtml += 'Без перерывов';
				} else {
					var isValid = true;
					isValid &= (new RegExp(TIME_PATTERN).test(bt[0]));
					isValid &= (new RegExp(TIME_PATTERN).test(bt[1])); 
					if (!isValid) {
						rawHtml += '<span style="color: red;">'
					}
					rawHtml += '(перерыв): ' 
						+ bt[0] + ' - ' + bt[1];
					if (!isValid) {
						rawHtml += '</span>';
						if (errorMessage != '') {
							errorMessage += '<br>';
						}
						errorMessage += 'Ошибка ввода: ' + 
							DAY_OF_WEEK[outDay].large;
					}
				}
				rawHtml += '</span>';
				if ((bi+1 != dayOfWeekModels[i]
					[DAY_OF_WEEK[outDay].short].length) || (outDay != 'ВС')) {
					rawHtml += '<br>';
				}
			}
		}
		if (errorMessage != '') {
			rawHtml = '<span style="color: red;" class="preview_row">'
				+ errorMessage + '</span><br>' + rawHtml;
		}
		$(idPreviewWrapper).html(rawHtml); 

	}
}

function isNone(value) {
	//return !value;
	return "NONE" == value;
}
