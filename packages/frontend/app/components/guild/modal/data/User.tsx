import { DataComponentProps } from "@/app/types";
import { Button, Col, Row } from "react-bootstrap";

export default function User({ data, setGuild, setData }: DataComponentProps) {
  const deleteUser = () => {
    // TODO: call delete api, then validate and setguild + setdata
  };

  return (
    <>
      <Row>
        <Col>{JSON.parse(data.body).id}</Col>
      </Row>
      <Row>
        <Col>
          <Button
            className="authButton"
            style={{ position: "absolute", bottom: 10 }}
            onClick={deleteUser}
          >
            delete user
          </Button>
        </Col>
      </Row>
    </>
  );
}
