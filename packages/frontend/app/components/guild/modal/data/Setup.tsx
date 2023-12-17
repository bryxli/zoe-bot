import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/app/types";

export default function Setup({ data, setGuild, setData }: DataComponentProps) {
  const setup = (event: any) => {
    event.preventDefault();

    const id = event.target.id.value;
  };

  return (
    <Form onSubmit={setup}>
      <Form.Group className="mb-3">
        <Form.Control name="id" placeholder="Discord Channel ID" />
        <br></br>
        <Button
          type="submit"
          className="authButton"
          style={{ position: "absolute", bottom: 10 }}
        >
          /setup
        </Button>
      </Form.Group>
    </Form>
  );
}
