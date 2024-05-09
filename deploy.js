import { exec } from "child_process";
import config from "./configs/config.json" with { type: "json" };

const deploy = (command, exitHandler) => {
  const output = (log) => {
    const pattern = /(InteractionsEndpoint|URL): https:\/\/[^\s]+/g;
  
    const output = {};
      
    let match;
    while ((match = pattern.exec(log)) !== null) {
      let obj = match[0].split(": ");
      if (obj[0] === "InteractionsEndpoints") {
        obj[1] = obj[1].replace("***", config.aws_region);
      }
      output[obj[0]] = obj[1]
    }
  
    return output;
  }

  let stdout = "";
  
  const child = exec(command);
  
  child.stdout.on("data", (data) => {
    stdout = stdout.concat(data)
    process.stdout.write(data);
  });
    
  child.stderr.on("data", (data) => {
    process.stderr.write(data);
  });
    
  child.on("error", (error) => {
    process.stderr.write(`Error executing initialization command: ${error}`);
  });
  
  child.on("exit", (exitCode, signal) => {
    if (exitCode === 0) {
      exitHandler(command, output(stdout));
    } else {
      process.stderr.write(`Deploy exited with code ${exitCode} and signal ${signal}`);
    }
  });
}

export { deploy };
