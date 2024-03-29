import Image from "next/image";

import { UserProps } from "@/types";

export default function User({ username, avatar, id }: UserProps) {
  return (
    <div data-testid="User">
      {id !== "" && avatar != "" && (
        <Image
          src={`https://cdn.discordapp.com/avatars/${id}/${avatar}.jpg`}
          alt="User Avatar"
          width={150}
          height={150}
          priority={true}
        />
      )}
      <p className="information">
        You have successfully signed in as <b>{username}</b>
      </p>
    </div>
  );
}
