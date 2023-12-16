import { Card } from "react-bootstrap";

import { DataProps } from "@/app/types";

export default function Data(data: DataProps) {
  const addUser = () => {
    // call adduser api endpoint
  };

  const delUser = () => {
    // call deluser api endpoint
  };

  const region = () => {
    // call region api endpoint
  };

  const setup = () => {
    // call setup api endpoint
  };

  return (
    <Card className="h-100">
      <Card.Header>
        <Card.Title>{data.command}</Card.Title>
      </Card.Header>
      <Card.Body>{data.body}</Card.Body>
    </Card>
  );
}
