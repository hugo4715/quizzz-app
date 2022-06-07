<template>
  <div>
    <slot></slot>
    <div id="threejs-container"></div>
  </div>
</template>

<script>
import * as THREE from "three";
import {RoomEnvironment} from "three/examples/jsm/environments/RoomEnvironment";
import {Vector3} from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
import {DRACOLoader} from "three/examples/jsm/loaders/DRACOLoader";
import {GLTFLoader} from "three/examples/jsm/loaders/GLTFLoader";

export default {
  name: "Background3D",
  mounted(){

//THREE JS

    let mixer;
    const clock = new THREE.Clock();
    const container = document.getElementById( 'threejs-container' );

    const renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.outputEncoding = THREE.sRGBEncoding;
    container.appendChild( renderer.domElement );

    const pmremGenerator = new THREE.PMREMGenerator( renderer );

    const scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xbfe3dd );
    scene.environment = pmremGenerator.fromScene( new RoomEnvironment(), 0.04 ).texture;



    var cameraPositions = [
      new Vector3(0, 0, 6 ),
      new Vector3(6,0,0),
      new Vector3(1, 0, -6 ),
      new Vector3(-6, 0, 0 ),

    ]
    window.cameraPositionIndex = 0;

// skybox
    const skyboxloader = new THREE.CubeTextureLoader();
    const texture = skyboxloader.load([
      'Skybox/px.png',
      'Skybox/nx.png',
      'Skybox/py.png',
      'Skybox/ny.png',
      'Skybox/pz.png',
      'Skybox/nz.png',
    ]);
    scene.background = texture;

    const camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 1, 100 );
    camera.position.set( 0, 0, 6 );

    const controls = new OrbitControls( camera, renderer.domElement );
    controls.target.set( 0, 0.5, 0 );
    controls.update();
    controls.enablePan = false;
    controls.enableDamping = true;

    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath( '/draco/' );

    const loader = new GLTFLoader();
    loader.setDRACOLoader( dracoLoader );
    loader.load( '/LittlestTokyo.glb', function ( gltf ) {
      const model = gltf.scene;
      model.position.set( 1, 1, 0 );
      model.scale.set( 0.01, 0.01, 0.01 );
      scene.add( model );

      mixer = new THREE.AnimationMixer( model );
      mixer.clipAction( gltf.animations[ 0 ] ).play();

      animate();
    }, undefined, function ( e ) {
      console.error( e );
    } );


    window.onresize = function () {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize( window.innerWidth, window.innerHeight );
    };

    function animate() {
      requestAnimationFrame( animate );
      const delta = clock.getDelta();

      let nextPos = cameraPositions[window.cameraPositionIndex];
      if(camera.position !== nextPos){
        camera.position.lerp(nextPos, .01);
      }

      mixer.update( delta );
      controls.update();
      //stats.update();
      renderer.render( scene, camera );
    }

    window.cameraNextPosition = function(){
      if(window.cameraPositionIndex  === cameraPositions.length -1)window.cameraPositionIndex = 0;
      else window.cameraPositionIndex++;
    }
  }
}
</script>

<style scoped>

</style>