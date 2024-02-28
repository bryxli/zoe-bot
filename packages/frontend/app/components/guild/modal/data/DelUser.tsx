import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function DelUser({
  data,
  setGuild,
  setData,
}: DataComponentProps) {
  const deluser = (event: any) => {
    event.preventDefault();

    const name = event.target.name.value;

    // TODO: call deluser
  };

  return (
    <div data-testid="DelUser">
      <Form onSubmit={deluser}>
        <Form.Group className="mb-3">
          <Form.Control name="name" placeholder="League username" />
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
