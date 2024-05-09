import { deploy } from "./deploy.js"

let res;

const exitHandler = (command, output) => {
  if (command.includes("WebStack")) {
    console.log(res);
  } else {
    res = output;

    // TODO: write url to file

    deploy("sst deploy WebStack --stage prod", exitHandler);
  }
}

deploy("sst deploy --stage prod", exitHandler)
