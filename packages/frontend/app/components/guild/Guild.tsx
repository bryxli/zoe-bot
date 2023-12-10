"use client";

import { useState } from "react";
import { Card } from "react-bootstrap";
import { GuildProps } from "../../types";
import GuildModal from "./Modal";

export default function Guild({
  id,
  name,
  icon,
  owner,
  permissions,
  permissions_new,
  features,
}: GuildProps) {
  const [showModal, setShowModal] = useState(false);

  const display = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <Card className="h-100" style={{ cursor: "pointer" }} onClick={display}>
        <Card.Body className="d-flex align-items-center justify-content-center text-center">
          <Card.Title> {name} </Card.Title>
        </Card.Body>
      </Card>
      <GuildModal
        showModal={showModal}
        onHide={display}
        id={id}
        name={name}
        icon={icon}
      />
    </>
  );
}
