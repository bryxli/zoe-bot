import { deploy } from "./deploy.js"

const exitHandler = (command, output) => {
  console.log(output);
}

deploy("sst deploy --stage dev", exitHandler)
