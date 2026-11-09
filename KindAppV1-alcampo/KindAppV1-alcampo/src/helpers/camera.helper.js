

export const capturePhoto = async () => {
  let camera = navigator.camera;
  if (!camera) return { error: "No fue posible acceder a la cámara, asegurese de haber proveido los permisos necesarios y vuelva a intentarlo." }
  const options = {
    quality: 20,
    destinationType: camera.DestinationType.DATA_URL,
    encodingType: camera.EncodingType.JPG,
    mediaType: camera.MediaType.PICTURE,
    saveToPhotoAlbum: false,
    correctOrientation: true
  };
  try {
    return await new Promise((resolve, reject) => {
      camera.getPicture(
        data => resolve({ data: `${data}` }),
        error => reject("No se pudo al capturar la foto, por favor vuelva a intentarlo."),
        options
      )
    })
  }
  catch (error) { return { error } }
}