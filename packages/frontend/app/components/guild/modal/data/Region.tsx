import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function Region({
  data,
  setGuild,
  setData,
}: DataComponentProps) {
  const region = (event: any) => {
    event.preventDefault();

    const region = event.target.name.value;
  };

  return (
    <Form onSubmit={region}>
      <Form.Group className="mb-3">
        <Form.Control name="name" placeholder="Region" />
        <br></br>
        <Button
          type="submit"
          className="authButton"
          style={{ position: "absolute", bottom: 10 }}
        >
          /region
        </Button>
      </Form.Group>
    </Form>
  );
}
