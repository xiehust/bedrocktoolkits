//import cloudscape libraries

//create a funtion to generate random Id
function generateUniqueId(){
    const timestamp = Date.now();
  const randomNumber = Math.random();
  //convert the random number to hexadecimal string
  const hexadecimalString = randomNumber.toString(16);
  return `id-${timestamp}-${hexadecimalString}`;
}

