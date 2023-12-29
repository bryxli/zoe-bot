import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Logout from "@/logout/page";

describe("Logout", () => {
  it("renders Logout", () => {
    render(
      <AuthProvider>
        <GuildProvider>
          <Logout />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Logout");

    expect(component).toBeInTheDocument();
  });
});
