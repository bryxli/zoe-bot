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
  };

  return (
    <div data-testid="DelUser">
      <Form onSubmit={deluser}>
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
    </div>
  );
}
