document.addEventListener('DOMContentLoaded',domloaded,false);
function domloaded(){
	var mbW=document.getElementById("myCanvas");
	var mbWx=mbW.getContext("2d");
	mbWx.moveTo(100,230);
	mbWx.lineTo(700,230);
	mbWx.stroke();

	var p1W=document.getElementById("myCanvas");
	var p1Wx=p1W.getContext("2d");
	p1Wx.moveTo(100,230);
	p1Wx.lineTo(100,150);
	p1Wx.stroke();

	var p2W=document.getElementById("myCanvas");
	var p2Wx=p2W.getContext("2d");
	p2Wx.moveTo(300,230);
	p2Wx.lineTo(300,150);
	p2Wx.stroke();

	var p3W=document.getElementById("myCanvas");
	var p3Wx=p3W.getContext("2d");
	p3Wx.moveTo(500,230);
	p3Wx.lineTo(500,150);
	p3Wx.stroke();

	var mmW=document.getElementById("myCanvas");
	var mmWx=mmW.getContext("2d");
	mmWx.strokeStyle="black";
	mmWx.moveTo(700,230);
	mmWx.lineTo(700,210);
	mmWx.stroke();

	var arc1=document.getElementById("myCanvas");
	var arc1tx=arc1.getContext("2d");
	arc1tx.strokeStyle="teal";
	arc1tx.beginPath();
	arc1tx.arc(100,50,50,Math.PI,2*Math.PI);
	arc1tx.stroke();

	var p1=document.getElementById("myCanvas");
	var p1x=p1.getContext("2d");
	p1x.font="10px Arial";
	p1x.fillText("Processor 1",75,30);

	var box1 = document.getElementById("myCanvas");
	var box1tx = box1.getContext("2d");
	box1tx.strokeStyle = "darkblue";
	box1tx.strokeRect(25,50,150,100);

	var arc2 = document.getElementById("myCanvas");
	var arc2tx = arc2.getContext("2d");
	arc2tx.strokeStyle="teal";
	arc2tx.beginPath();
	arc2tx.arc(300,50,50,Math.PI,2*Math.PI);
	arc2tx.stroke();

	var p2=document.getElementById("myCanvas");
	var p2x=p2.getContext("2d");
	p2x.font="10px Arial";
	p2x.fillText("Processor 2",275,30);

	var box2 = document.getElementById("myCanvas");
	var box2tx = box2.getContext("2d");
	box2tx.strokeStyle = "darkblue";
	box2tx.strokeRect(225,50,150,100);


	var arc3 = document.getElementById("myCanvas");
	var arc3tx = arc3.getContext("2d");
	arc3tx.strokeStyle="teal";
	arc3tx.beginPath();
	arc3tx.arc(500,50,50,Math.PI,2*Math.PI);
	arc3tx.stroke();

	var p3=document.getElementById("myCanvas");
	var p3x=p3.getContext("2d");
	p3x.font="10px Arial";
	p3x.fillText("Processor 3",475,30);

	var box3 = document.getElementById("myCanvas");
	var box3tx = box3.getContext("2d");
	box3tx.strokeStyle = "darkblue";
	box3tx.strokeRect(425,50,150,100);


	var mainbox = document.getElementById("myCanvas");
	var mainboxtx = mainbox.getContext("2d");
	mainboxtx.strokeStyle ="red";
	mainboxtx.strokeRect(625,10,150,200);

	var p4=document.getElementById("myCanvas");
	var p4x=p4.getContext("2d");
	p4x.font="10px Arial";
	p4x.fillText("Main Memory",630,20);
	
	var qt=document.getElementById("myCanvas");
	var qtx=qt.getContext("2d");
	qtx.font="20px Arial";
	qtx.fillText("Which of the following actions should the processor perform?",130,270);
	
	var st=document.getElementById("myCanvas");
	var stx=st.getContext("2d");
	stx.font="25px Arial";
	stx.fillText("A)GETS  B)GETX  C)UPGRADE  D)no coherence action",100,300);
}