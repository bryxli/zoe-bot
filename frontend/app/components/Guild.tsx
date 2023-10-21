"use client";

import { Card } from "react-bootstrap";

import { GuildProps } from "../types";

export default function Guild({
  id,
  name,
  icon,
  owner,
  permissions,
  permissions_new,
  features,
}: GuildProps) {
  return (
    <Card>
      <Card.Body>
        <Card.Title> {name} </Card.Title>
      </Card.Body>
    </Card>
  );
}
