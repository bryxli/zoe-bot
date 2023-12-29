import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import User from "@/components/User";

describe("Header", () => {
  it("renders Header", () => {
    const container = render(
      <AuthProvider>
        <GuildProvider>
          <User />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("User").length).toBe(1);
  });
});
