import { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import Image from "next/image";

import { GuildModalProps } from "../types";
import { getAllUsers } from "./Dynamo";

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
      try {
        const users = await getAllUsers(id);
        setUserlist(users || []);
      } catch (e) {
        setUserlist([]);
      }
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
