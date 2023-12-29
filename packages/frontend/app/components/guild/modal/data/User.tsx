import { Button, Col, Row } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function User({ data, setGuild, setData }: DataComponentProps) {
  const deleteUser = () => {
    // TODO: call delete api, then validate and setguild + setdata
  };

  return (
    <>
      <Row>
        <Col>{data.body.id}</Col>
      </Row>
      <br></br>
      <br></br>
      <Button
        className="authButton"
        style={{ position: "absolute", bottom: 10 }}
        onClick={deleteUser}
      >
        delete user
      </Button>
    </>
  );
}
