function rekamwajah() {
	eel.rekamwajah()
}

function catatKehadiran() {
	eel.catatKehadiran()
}

function register(){
	var nama = document.getElementById("nama").value;
	var nrp = document.getElementById("nrp").value;
	eel.register(nama,nrp)
}

function command(){
	var cmd = document.getElementById("command").value;
	var res = eel.execute(cmd);
	document.getElementById("result").innerText = res;
}