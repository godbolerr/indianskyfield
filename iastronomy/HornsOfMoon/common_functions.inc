
// common_functions.inc

// Utility funtions for Stellarium

var color="#00AAFF";

function hideLandscape() {
  LandscapeMgr.setFlagAtmosphere(false);
  LandscapeMgr.setFlagLandscape(false);
  LandscapeMgr.setFlagFog(false);
  LandscapeMgr.setFlagCardinalPoints(false);
}

function showLandscape() {
  LandscapeMgr.setFlagAtmosphere(true);
  LandscapeMgr.setFlagLandscape(true);
  LandscapeMgr.setFlagFog(true);
  LandscapeMgr.setFlagCardinalPoints(true);
}

// Returns ids of all the lables 
// Usage : ids = blockText(Array("Line1","Line 2"));

function blockText(textArray)
{
	var fontSize = 20;
	var lineSep = fontSize * 2;
	y = 50;
	ids = new Array();
	for(i=0; i<textArray.length; i++)
	{
		ids[i] = LabelMgr.labelScreen(textArray[i], 100, y, false, fontSize, "#FFFFFF");
		y += lineSep;
	}

	for(i=0; i<ids.length; i++)
	{
		LabelMgr.setLabelShow(ids[i], true);
		core.wait(0.15);
	}
	return ids;
}


function clearLabels(ids)
{
	for(i=0; i<ids.length; i++)
	{
		LabelMgr.setLabelShow(ids[i], false);
		core.wait(0.15);
	}
	core.wait(1);
	for(i=0; i<ids.length; i++)
	{
		LabelMgr.deleteLabel(ids[i]);
	}
}

// This function prints a line of text at a fixed place on the screen
// pauses for a few seconds and then hides the text.  I will use this
// for providing information to the user.
//
// The label is created in an "off" state, and then faded in and out.
// The label is deleted after it has been displayed.


function commentary(text)
{
	commentary_at(text, 30, 30);
}

function commentary_at(text, x, y)
{
	var id = LabelMgr.labelScreen(text, x, y, false, 30, "#aaaaaa");
	LabelMgr.setLabelShow(id, true);
	return id;
}



function showConstellation(cName, aFOV)
{
	core.selectObjectByName(cName, true);
	StelMovementMgr.autoZoomIn(5);
	core.wait(1);
	StelMovementMgr.zoomTo(aFOV,3);
	core.wait(1);
	ConstellationMgr.setFlagArt(true);
	core.wait(5);
	ConstellationMgr.setFlagArt(false);
}



function setStage()
{
	ConstellationMgr.setFlagLabels(false);
	SolarSystem.setFlagPlanets(true);
	LandscapeMgr.setFlagLandscape(true);
	LandscapeMgr.setFlagAtmosphere(true);
	LandscapeMgr.setFlagFog(true);
	StelMovementMgr.autoZoomIn(3);

	StelMovementMgr.setAutoMoveDuration(2);
	
	core.goHome();
	StelMovementMgr.autoZoomIn(1);
	core.setTimeRate(0);
	StelMovementMgr.deselection();
}

function goToNPole()
{
	LandscapeMgr.setFlagAtmosphere(false);
	LandscapeMgr.setFlagFog(false);
	core.setObserverLocation(15, 90 , 1,1,"","Earth");
}

function goToSPole()
{
	LandscapeMgr.setFlagAtmosphere(false);
	LandscapeMgr.setFlagFog(false);
	core.setObserverLocation(15, -90 , 1,1,"","Earth");
}

function nextActionLabel(description)
{
		txt1 = LabelMgr.labelScreen(description, 50, 20, false, 12, "#ffffff");
		LabelMgr.setLabelShow(txt1, true);
		core.wait(4);
		LabelMgr.setLabelShow(txt1, false);

}


// Press A key to proceed

function pause()
{
		// Keypress
		txt1 = LabelMgr.labelScreen("Press the A Key to continue", 50, 40, false, 20, "#FF00AA");
		LabelMgr.setLabelShow(txt1, true);

		kp = 0
		oa = LandscapeMgr.getFlagAtmosphere();


		while (kp == 0)
		{
		ca = LandscapeMgr.getFlagAtmosphere();
		core.wait(0.05); // This is needed in Stellarium version 1.0

		if (ca != oa)
		{
		kp = 1
		}


		}


		LandscapeMgr.setFlagAtmosphere(oa);
		
		LabelMgr.setLabelShow(txt1, false);

		// End Keypress
}

function justWait()
{
	core.wait(2);
}

function outAndIn(object)
{
	core.wait(2);
	StelMovementMgr.autoZoomOut(2);
	core.wait(1);
	StelMovementMgr.autoZoomOut(2);
	core.wait(2);
	core.selectObjectByName(object, false);
	StelMovementMgr.setFlagTracking(true);
	core.wait(0.5);
	StelMovementMgr.autoZoomIn(1);
	core.wait(0.5);
	StelMovementMgr.autoZoomIn(2);
	core.wait(0.5);
	StelMovementMgr.autoZoomIn(2);
	core.wait(0.5);
}

function locationInfo(){
	locationMap=core.getObserverLocationInfo();
	core.output("Location longitude: "           + locationMap["longitude"]);
	core.output("Location latitude: "            + locationMap["latitude"]);
	core.output("Location altitude: "            + locationMap["altitude"]);
	core.output("Location name: "                + locationMap["location"]);
	core.output("Location planet: "              + locationMap["planet"]);
	core.output("Location local-sidereal-time: " + locationMap["local-sidereal-time"]);
	core.output("Location Bortle Index: "        + core.getBortleScaleIndex());
}

function hideLandscape() {
  LandscapeMgr.setFlagAtmosphere(false);
  LandscapeMgr.setFlagLandscape(false);
  LandscapeMgr.setFlagCardinalPoints(false);
}

function pauseA()
{

	var pauseLabel = LabelMgr.labelScreen("Press A to continue",50,100,true,20,"#ff0000");

	kp = 0
	oa = LandscapeMgr.getFlagAtmosphere();


	while (kp == 0)
	{
		ca = LandscapeMgr.getFlagAtmosphere();
		core.wait(0.05); // This is needed in Stellarium version 1.0

		if (ca != oa)
		{
			kp = 1
		}

	}
	
	LandscapeMgr.setFlagAtmosphere(oa);

	LabelMgr.deleteLabel(pauseLabel);
	return;
}

function initStellarium()
{
	core.wait(0.5);
	LabelMgr.deleteAllLabels();
	MarkerMgr.deleteAllMarkers();
	core.wait(0.5);
	core.goHome();
	var color = "#ffffff";
	core.setGuiVisible(false);
	core.setTimeRate(1);
	core.clear("natural");
	LandscapeMgr.setFlagCardinalPoints(true);
}

function displayDateTimeLoop(){

timeLabel = LabelMgr.labelScreen("", 500, 10, true, 15, "#FFFFFF");
core.setDate("2012-06-05T22:09:00", "utc");
while(true) {
LabelMgr.setLabelText(timeLabel,core.getDate());
core.wait(1);
}

}

function tr(str)
{
	return core.translate(str);
}

function resetStellarium()
{
	core.wait(0.5);
	LabelMgr.deleteAllLabels();
	MarkerMgr.deleteAllMarkers();
	core.wait(0.5);
	core.goHome();
	var color = "#ffffff";
	core.setGuiVisible(true);
	core.setTimeRate(1);
	LandscapeMgr.setFlagCardinalPoints(false);
}

function goToEquatorPrimeMeridian()
{
	core.setObserverLocation(0.0, 0.0, 0, 1, "Equator/Prime Meridian", "Earth");
}

//
// Name: common objects include file
// License: Public Domain

var planets = new Array("Sun", "Mercury", "Venus", "Moon", "Mars", 
"Jupiter",  "Saturn","Uranus","Neptune"); 


var nakAllStarList = 
[["1","Ashwini","1.1","HIP8832","HR 546","अश्विनी" ],
["2","Ashwini","1.2","HIP8903","HR 553","अश्विनी" ],
["3","Bharani","2.1","HIP12719","HR 801","भरणी" ],
["4","Bharani","2.2","HIP13061","HR 824","भरणी" ],
["5","Bharani","2.3","HIP13209","HR 838","भरणी" ],
["6","Kruttika","3.1","HIP17499","hr 1142","कृत्तिका" ],
["7","Kruttika","3.2","HIP17531","HR 1145","कृत्तिका" ],
["8","Kruttika","3.3","HIP17573","hr 1149","कृत्तिका" ],
["9","Kruttika","3.4","HIP17579","hr 1151","कृत्तिका" ],
["10","Kruttika","3.5","HIP17608","hr 1156","कृत्तिका" ],
["11","Kruttika","3.6","HIP17702","hr 1165","कृत्तिका" ],
["12","Kruttika","3.7","HIP17847","hr 1178","कृत्तिका" ],
["13","Kruttika","3.8","HIP17851","HR 1180","कृत्तिका" ],
["14","Rohini","4","HIP21421","hr 1457","रोहिणी" ],
["15","Mrugshirsha","5.1","HIP26176","hr 1876","मृगशिरा" ],
["16","Mrugshirsha","5.2","HIP26207","hr 1879","मृगशिरा" ],
["17","Mrugshirsha","5.3","HIP26366","hr 1907","मृगशिरा" ],
["18","Adra","6","HIP27989","hr 2061","आर्द्रा" ],
["19","Punarvasu","7.1","HIP36850","hr 2890","पुनर्वसु" ],
["20","Punarvasu","7.2","HIP37826","hr 2990","पुनर्वसु" ],
["21","Pushya","8.1","HIP41822","hr 3357","पुष्या" ],
["22","Pushya","8.2","HIP42806","hr 3449","पुष्या" ],
["23","Pushya","8.3","HIP42911","hr 3461","पुष्या" ],
["24","Ashlesha","9.1","HIP42313","3410","आश्लेषा" ],
["25","Ashlesha","9.2","HIP42402","3418","आश्लेषा" ],
["26","Ashlesha","9.3","HIP42799","3454","आश्लेषा" ],
["27","Ashlesha","9.4","HIP43109","3482","आश्लेषा" ],
["28","Ashlesha","9.5","HIP43234","3492","आश्लेषा" ],
["29","Magha","10","HIP49669","3982","मघा" ],
["30","PurvFalguna","11.1","HIP54872","4357","पूर्वफल्गुनी" ],
["31","PurvFalguna","11.2","HIP54879","4359","पूर्वफल्गुनी" ],
["32","UttarFalguna","12.1","HIP57632","4534","उत्तरफल्गुनी" ],
["33","Hasta","13.1","HIP59199","4623","हस्ता" ],
["34","Hasta","13.2","HIP59316","4630","हस्ता" ],
["35","Hasta","13.3","HIP59803","4662","हस्ता" ],
["36","Hasta","13.4","HIP60965","4757","हस्ता" ],
["37","Hasta","13.5","HIP61359","4786","हस्ता" ],
["38","Chitra","14","HIP65474","5056","चित्रा" ],
["39","Swati","15","HIP69673","5340","स्वातिः" ],
["40","Vishakha","16.1","HIP72622","5531","विशाखा" ],
["41","Vishakha","16.2","HIP74392","5652","विशाखा" ],
["42","Vishakha","16.3","HIP74785","5685","विशाखा" ],
["43","Vishakha","16.4","HIP76333","5787","विशाखा" ],
["44","Anuradha","17.1","HIP78265","5944","अनुराधा" ],
["45","Anuradha","17.2","HIP78401","5953","अनुराधा" ],
["46","Anuradha","17.3","HIP78820","5984","अनुराधा" ],
["47","Jeshtha","18.1","HIP80112","6084","ज्येष्ठा" ],
["48","Jeshtha","18.2","HIP80763","6134","ज्येष्ठा" ],
["49","Jeshtha","18.3","HIP81266","6165","ज्येष्ठा" ],
["50","Mula","19.1","HIP82396","6241","मूला" ],
["51","Mula","19.2","HIP82545","6252","मूला" ],
["52","Mula","19.3","HIP82729","6271","मूला" ],
["53","Mula","19.4","HIP84143","6380","मूला" ],
["54","Mula","19.5","HIP85696","6508","मूला" ],
["55","Mula","19.6","HIP85927","6527","मूला" ],
["56","Mula","19.7","HIP86228","6553","मूला" ],
["57","Mula","19.8","HIP86670","6580","मूला" ],
["58","Mula","19.9","HIP87073","6615","मूला" ],
["59","Purvashadha","20.1","HIP89931","6859","पूर्वाषाढा" ],
["60","Purvashadha","20.2","HIP90185","6879","पूर्वाषाढा" ],
["61","Uttarashadha","21.1","HIP92855","7121","उत्तराषाढा" ],
["62","Uttarashadha","21.2","HIP93506","7194","उत्तराषाढा" ],
["63","Shravan","22.1","HIP97278","7525","श्रवणा" ],
["64","Shravan","22.2","HIP97649","7557","श्रवणा" ],
["65","Shravan","22.3","HIP98036","7602","श्रवणा" ],
["66","Dhanishtha","23.1","HIP101958 ","7906","धनिष्ठा" ],
["67","Dhanishtha","23.2","HIP102281","7928","धनिष्ठा" ],
["68","Shatataraka","24","HIP110395","8518","शतभिषा " ],
["69","PurvBhadrapada","25.1","HIP113881","8775","पूर्वभाद्रपदा" ],
["70","PurvBhadrapada","25.2","HIP113963","8781","पूर्वभाद्रपदा" ],
["71","UttarBhadrapada","26.1","HIP677","15","उत्तरभाद्रपदा" ],
["72","UttarBhadrapada","26.2","HIP1067","39","उत्तरभाद्रपदा" ],
["73","Revati","27","HIP5737","361" ,"रेवती" ]];

// RA, DE, FOV, Name, HIP, Note


var yogataras = [["1","Ashwini","1.1","HIP8832","HR 546","अश्विनी"],
["2","Bharani","2.1","HIP12719","HR 801","भरणी "],
["3","Kruttika","3.1","HIP17499","hr 1142","कृत्तिका "],
["4","Rohini","4","HIP21421","hr 1457","रोहिणी "],
["5","Mrugshirsha","5.1","HIP26176","hr 1876","मृगः "],
["6","Adra","6","HIP27989","hr 2061","आर्द्रा "],
["7","Punarvasu","7.1","HIP36850","hr 2890","पुनर्वसु "],
["8","Pushya","8.1","HIP41822","hr 3357","पुष्य"],
["9","Ashlesha","9.1","HIP42313","3410","आश्लेषा "],

["10","Magha","10","HIP49669","3982","मघा "],
["11","PurvFalguna","11.1","HIP54872","4357","पूर्वाफाल्गुनी"],

["12","UttarFalguna","12.1","HIP57632","4534","उत्तराफाल्गुनी "],
["13","Hasta","13.1","HIP59199","4623","हस्त"],
["14","Chitra","14","HIP65474","5056","चित्रा "],
["15","Swati","15","HIP69673","5340","स्वाती "],
["16","Vishakha","16.1","HIP72622","5531","विशाखा "],
["17","Anuradha","17.1","HIP78265","5944","अनुराघा "],
["18","Jeshtha","18.1","HIP80112","6084","ज्येष्ठा "],
["19","Mula","19.1","HIP82396","6241","मूला"],
["20","Purvashadha","20.1","HIP89931","6859","पूर्वाषाढा "],
["21","Uttarashadha","21.1","HIP92855","7121","उत्तराषाढा "],

["22","Shravan","22.3","HIP98036","7602","श्रवण"],
["23","Dhanishtha","23.1","HIP101958 ","7906","घनिष्ठा "],
["24","Shatataraka","24","HIP110395","8518","शततारका"],
["25","PurvBhadrapada","25.1","HIP113881","8775","पूर्वभाद्रपदा"],
["26","UttarBhadrapada","26.1","HIP677","15","उत्तरभाद्रपदा"],
["27","Revati","27","HIP5737","361","रेवती"] ];



var astrolabeStars = [["1","Alpheratz","99.99","HIP677","Andromeda","उत्तराभाद्रप  "],
["26","Altair","99.99","HIP97649","Aquilla","श्रवण"],
["26","Hamal","99.99","HIP9884","Aries","मेष"],
["26","Capella","99.99","HIP24608","Auriga","ब्रह्महृदय"],
["26","Arcturus","99.99","HIP69673","Bootes","स्वातिः"],
["26","Sirius","99.99","HIP32349","Canis-major","व्याध"],
["26","Castor","99.99","HIP36850","Gemini","पुनर्वसु 0"],
["26","Pollux","99.99","HIP37826","Gemini","पुनर्वसु"],
["26","Regulus","99.99","HIP49669","Leo","मघा"],
["26","Vega","99.99","HIP91262","Lyra","अभिजित"],
["26","Betelgeuse","99.99","HIP27989","Orion","आर्द्रा"]];


function showNakshatra(cObject, aFOV,i)
{
	var info = core.getObjectInfo(cObject[i][3]);
	
	core.selectObjectByName(cObject[i][3], true);
	
	var id = LabelMgr.labelScreen(cObject[i][1] + " - " + cObject[i][5]  , 20, 120, false, 30, "#00AAFF");
       var id1 = LabelMgr.labelScreen(" E Long: " + info.elong  , 20, 160, false, 30, "#00CCFF");
       var id2 = LabelMgr.labelScreen( " E Lat: " + info.elat , 20, 190, false, 30, "#00AAFF");
       var id3 = LabelMgr.labelScreen( " V Mag: " + info.vmag , 20, 230, false, 30, "#11AAFF")
       var id4 = LabelMgr.labelScreen( " Name: " + info.name , 20, 360, false, 30, "#55AAFF")
	

LabelMgr.setLabelShow(id, true);
LabelMgr.setLabelShow(id1, true);
LabelMgr.setLabelShow(id2, true);
LabelMgr.setLabelShow(id3, true);
LabelMgr.setLabelShow(id4, true);

	StelMovementMgr.autoZoomIn(1);
	core.wait(3);
	StelMovementMgr.zoomTo(aFOV,4);
	var color = "#ff9900";
	var label = LabelMgr.labelObject(cObject[i][5],cObject[i][3], true, 16, color, "SE");
	LabelMgr.setLabelShow(label, true);
	core.wait(3);
	LabelMgr.setLabelShow(label, false);
	LabelMgr.setLabelShow(id, false);
	LabelMgr.setLabelShow(id1, false);
	LabelMgr.setLabelShow(id2, false);
	LabelMgr.setLabelShow(id3, false);
	LabelMgr.setLabelShow(id4, false);
}



function showNakshatraOnEcliptic(cObject, aFOV,i)
{
	var info = core.getObjectInfo(cObject[i][3]);
	core.selectObjectByName(cObject[i][3], true);
	var color = "#ff9900";
	var label = LabelMgr.labelObject(cObject[i][5],cObject[i][3], true, 16, color, "SE");
	LabelMgr.setLabelShow(label, true);
	core.wait(3);
}






