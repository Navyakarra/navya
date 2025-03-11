for (let i = 1; i <= 10; i++) {
    if (i === 5) {
      console.log(`Skipping ${i} with continue`);
      continue;
    }
  
    if (i === 8) {
      console.log(`Breaking the loop at ${i}`);
      break;
    }
  
    console.log(i);
  }
  