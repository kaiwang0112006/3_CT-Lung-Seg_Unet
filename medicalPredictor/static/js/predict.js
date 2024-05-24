function niipredict(){
    var filename = $('#filename').text();
	$.ajax({
		data: JSON.stringify({'filename':filename}),
		type: "POST",
		dataType: "json",
		url: '/predict_nii',
		beforeSend: function(){
        	document.getElementById('loading').innerHTML="<img alt='picture Not exist' src=\"" + "/static/image/loading.gif" + "\">";
        },
		success: function(data){
		        document.getElementById('loading').innerHTML=""
				$("#pred").html("pred="+data["pred"]+",  score="+data["score"])
		}
    });
    image = "/tmp/"+filename
    // create and initialize a 3D renderer
    var r = new X.renderer3D();
    r.init();

    // create a new X.mesh
    var skull = new X.mesh();
    // .. and associate the .vtk file to it
    // skull.file = 'http://x.babymri.org/?skull.vtk';    // Online Link
    skull.file = image;                                 // Downloaded Image - upload your VTK file and pass it here
    //skull.file = 'http://people.sc.fsu.edu/~lb13f/projects/finite_difference/three_js/cavity_test_7.vtk';
    // .. make it transparent
    skull.opacity = 0.7;

    // .. add the mesh
    r.add(skull);

    // re-position the camera to face the skull
    r.camera.position = [0, 400, 0];

    // animate..
    r.onRender = function() {

    // rotate the skull around the Z axis
    // since we moved the camera, it is Z not X
    skull.transform.rotateZ(1);

    // we could also rotate the camera instead which is better in case
    // we have a lot of objects and want to rotate them all:
    //
    // r.camera.rotate([1,0]);

    };

    r.render();
}
