import { useState } from "react";

export default function SearchBox() {
  const [search, setSearch] = useState<string>("");

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const arg = event.target.value;
    setSearch(arg);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // prevents reload

    // TODO: seach database for guild id, check if user is authenticated with guild

    console.log(search);
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Server ID"
          value={search}
          onChange={handleSearch}
        />
      </form>
    </>
  );
}
