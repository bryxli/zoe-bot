import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Logout from "@/logout/page";

describe("Logout", () => {
  it("renders Logout", () => {
    const container = render(
      <AuthProvider>
        <GuildProvider>
          <Logout />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("Logout").length).toBe(1);
  });
});
