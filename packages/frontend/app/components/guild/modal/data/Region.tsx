import { Button, Form } from "react-bootstrap";

import { DataComponentProps } from "@/types";

export default function Region({
  data,
  setGuild,
  setData,
}: DataComponentProps) {
  const region = (event: any) => {
    event.preventDefault();

    const region = event.target.region.value;

    // TODO: call region
  };

  return (
    <div data-testid="Region">
      <Form onSubmit={region}>
        <Form.Group className="mb-3">
          <Form.Control
            name="region"
            placeholder="WARNING: this will delete all users; region must be valid"
          />
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
    </div>
  );
}
