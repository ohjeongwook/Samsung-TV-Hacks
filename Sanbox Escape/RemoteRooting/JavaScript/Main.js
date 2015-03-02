var Main = { }

var widgetAPI = new Common.API.Widget();
var tvKey = new Common.API.TVKeyValue();

var filePlugin;
var currentStep = 0;
var logMessage = "";

var packagePath = '/mtd_rwcommon/common/TempDownLoad/Dropper';
var skypePath = '/mtd_rwcommon/moip/engines/Skype';

Main.onLoad = function() {
	document.getElementById("anchor").focus();
	filePlugin = document.getElementById("pluginFileSystem");
	showTitle();
	widgetAPI.sendReadyEvent();
};

Main.onUnload = function(){ };

Main.keyDown = function() {
	var keyCode = event.keyCode;
	switch(keyCode) {
		case tvKey.KEY_RETURN:
		case tvKey.KEY_PANEL_RETURN:
			clearLog();
			widgetAPI.sendReturnEvent();
			break;
		case tvKey.KEY_UP:
		case tvKey.KEY_PANEL_UP:
			clearLog();
			break;
		case tvKey.KEY_ENTER:
		case tvKey.KEY_PANEL_ENTER:
			if (currentStep == 0) {
				clearLog();
				setupSamyGO(packagePath);
			} else if (currentStep == 2) {
				rootSamyGO(packagePath);
			} else if (currentStep == 7) logPara("<b style='color:green'>SamyGO already activated!</b>");
			else logPara("<b style='color:red'>SamyGO not activated! Check for errors!<b/>");
			break;
		default:
			break;
	} 
};

function showTitle() {
	var titleDivElement = document.getElementById("title");
	var title = "Widget <b style='color:green'>" + curWidget.id + "</b> for Samsung SmartTV F-series";
	widgetAPI.putInnerHTML(titleDivElement, title);
	if ("SamyGO" == curWidget.id) {
		logPara("Press <b style='color:red'>Enter</b> for activation " + curWidget.id + "!");
	} else {
		logPara("Current widget name '<b style='color:red'>" + curWidget.id + "</b>' differs from expected 'SamyGO'!");
	}
};

function log(message) {
	var logDivElement = document.getElementById("log");
	logMessage = logMessage + message + "<br>";
	widgetAPI.putInnerHTML(logDivElement, logMessage);
};

function logPara(message) {
	var logDivElement = document.getElementById("log");
	logMessage = logMessage + "<p>" + message + "</p>";
	widgetAPI.putInnerHTML(logDivElement, logMessage);
};

function clearLog() {
	var logDivElement = document.getElementById("log");
	logMessage = "";
	widgetAPI.putInnerHTML(logDivElement, logMessage);
};

function setupSamyGO(path) {
	logPara("*********************** Setup SamyGO files *************************************");

	var skypeNotFound = false;
	currentStep += exists(skypePath + '/libSkype.so');
	if (currentStep != 1) {
		skypeNotFound = true;
	};
	exists(skypePath + "/AutoStart");
	exists(skypePath + "/runSamyGO.sh");
	exists(skypePath + "/remoteSamyGO.zip");
	currentStep += exists(packagePath + "/data/patch");

	if (currentStep == 2) {
		logPara("<span style='color:green'>All activation files found on: '"+ packagePath + "'</span>");
		logPara("Press <b style='color:red'>Enter</b> for activation " + curWidget.id + "!");
	} else {
		if (skypeNotFound) { 
			logPara("<span style='color:red'>Skype not found. Read Skype installation procedure.</span>");
		} else {
			logPara("<span style='color:red'>Some activation files not found on: '" + packagePath + "'</span>");
		}
		currentStep = -1;
	}
};

function rootSamyGO(path) {
	logPara("*********************** Root SamyGO files **************************************");

	currentStep += unzip(packagePath +"/data/patch", skypePath + "/");
	currentStep += exists(skypePath + "/libSkype.so");
	currentStep += exists(skypePath + "/AutoStart");
	currentStep += exists(skypePath + "/runSamyGO.sh");
	currentStep += exists(skypePath + "/remoteSamyGO.zip");

	if (currentStep == 7) {
		logPara("<span style='color:green'>All activation files processed.</span>");
		logPara("<b style='color:green'>Now press exit and restart TV then test FTP</b>");
	} else {
		logPara("<span style='color:red'>Some activation files not processed.</span>");
		logPara("<b style='color:red'>Read the rooting procedure.</b>");
		currentStep = -1;
	}
	log("Free memory: " + Math.round((filePlugin.GetTotalSize() - filePlugin.GetUsedSize())/1048576) + " Mbytes");
};

function status(result) {
	var color = (result == 1 ? "green" : "red");
	return "<span style='color:" + color +"'>" + (result == 1 ? "[OK]" : "[NO]") + "</span>";
};

function exists(from) {
	var command = "filePlugin.IsExistedPath('" + from + "')";
	var result = eval(command);
	log("Existing '" + from + "' ? " + status(result));
	return result;
};

function unzip(from, to) {
	var command = "filePlugin.Unzip('" + from + "', '" + to + "')";
	var result = eval(command);
	log("Extracted '" + from + "' to '" + to +"' ? " + status(result));
	return result;
};
