import React, { useState } from 'react';
import pica from 'pica';

const App = () => {
  const [imageSrc, setImageSrc] = useState(null);
  const [hexArray, setHexArray] = useState([]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setImageSrc(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const processImage = async () => {
    if (!imageSrc) return;

    const img = new Image();
    img.src = imageSrc;
    img.onload = async () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      const picaInstance = pica();
      const resizedCanvas = document.createElement('canvas');
      resizedCanvas.width = 28;
      resizedCanvas.height = 28;
      await picaInstance.resize(canvas, resizedCanvas);

      const resizedCtx = resizedCanvas.getContext('2d');
      const imageData = resizedCtx.getImageData(0, 0, 28, 28);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = data[i + 1] = data[i + 2] = avg;
      }
      resizedCtx.putImageData(imageData, 0, 0);

      const hexArray = [];
      for (let y = 0; y < 28; y++) {
        for (let x = 0; x < 28; x++) {
          const pixelData = resizedCtx.getImageData(x, y, 1, 1).data;
          const hex = rgbToHex(pixelData[0], pixelData[1], pixelData[2]);
          hexArray.push(hex);
        }
      }

      setHexArray(hexArray);
    };
  };

  const rgbToHex = (r, g, b) => {
    return `#${componentToHex(r)}${componentToHex(g)}${componentToHex(b)}`;
  };

  const componentToHex = (c) => {
    const hex = c.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Image to Grayscale Hex Array</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <br />
      {imageSrc && (
        <div>
          <img src={imageSrc} alt="Uploaded" style={{ maxWidth: '300px', marginTop: '20px' }} />
          <br />
          <button onClick={processImage} style={{ marginTop: '20px' }}>Process Image</button>
        </div>
      )}
      {hexArray.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h2>Hex Color Array</h2>
          <pre>{JSON.stringify(hexArray, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default App;
