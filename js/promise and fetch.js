let myPromise = new Promise((resolve, reject) => {
    let success = true;
    
    if (success) {
      resolve("Operation succeeded!");
    } else {
      reject("Operation failed!");
    }
  });
  
  myPromise
    .then((result) => {
      console.log(result);
    })
    .catch((error) => {
      console.log(error);
    });
  