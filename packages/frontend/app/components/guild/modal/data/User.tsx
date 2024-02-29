import { Button, Col, Form, Row } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function User({ data, setGuild, setData }: DataComponentProps) {
  const deluser = (event: any) => {
    event.preventDefault();

    const nameToCheck = data.body.name;
    const name = event.target.name.value;

    if (name === nameToCheck) {
      // TODO: call deluser
    }
  };

  return (
    <div data-testid="User">
      <Form onSubmit={deluser}>
        <Form.Group className="mb-3">
          <Form.Control
            name="name"
            placeholder="Please type in username to confirm deletion"
          />
          <br></br>
          <Button
            type="submit"
            className="authButton"
            style={{ position: "absolute", bottom: 10 }}
          >
            /deluser
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}
