import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/app/types";

export default function AddUser({
  data,
  setGuild,
  setData,
}: DataComponentProps) {
  const adduser = (event: any) => {
    event.preventDefault();

    const name = event.target.name.value;
  };

  return (
    <Form onSubmit={adduser}>
      <Form.Group className="mb-3">
        <Form.Control name="name" placeholder="League Username" />
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
  );
}
