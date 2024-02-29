import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function AddUser({
  data,
  setGuild,
  setData,
}: DataComponentProps) {
  const adduser = (event: any) => {
    event.preventDefault();

    const name = event.target.name.value;

    // TODO: call adduser
  };

  return (
    <div data-testid="AddUser">
      <Form onSubmit={adduser}>
        <Form.Group className="mb-3">
          <Form.Control name="name" placeholder="League username" />
          <br></br>
          <Button
            type="submit"
            className="authButton"
            style={{ position: "absolute", bottom: 10 }}
          >
            /adduser
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}
