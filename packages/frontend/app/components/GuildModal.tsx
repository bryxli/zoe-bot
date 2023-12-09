import { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import Image from "next/image";

import { GuildModalProps } from "../types";

export default function GuildModal({
  showModal,
  onHide,
  id,
  name,
  icon,
}: GuildModalProps) {
  const [userlist, setUserlist] = useState<string[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      await fetch("/api/dynamo")
        .then((result) => result.json())
        .then((response) => {
          setUserlist(response);
        });
    };

    fetchUsers();
  }, [id]);

  return (
    <Modal show={showModal} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>
          {name}
          {icon && (
            <Image
              src={`https://cdn.discordapp.com/icons/${id}/${icon}.jpg`}
              alt="Guild Avatar"
              width={30}
              height={30}
              priority={true}
            />
          )}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {userlist.length > 0 ? <>{userlist}</> : <>userlist is empty</>}
      </Modal.Body>
    </Modal>
  );
}
