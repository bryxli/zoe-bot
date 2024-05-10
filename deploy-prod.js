import { writeFile } from "fs/promises";
import { deploy } from "./deploy.js"

let res;

const exitHandler = (command, output) => {
  if (command.includes("WebStack")) {
    console.log(res);
  } else {
    res = output;

    writeFile("deploy-prod.json", JSON.stringify(output));

    deploy("sst deploy WebStack --stage prod", exitHandler);
  }
}

deploy("sst deploy --stage prod", exitHandler)
