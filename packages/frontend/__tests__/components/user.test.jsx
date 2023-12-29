import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import User from "@/components/User";

describe("User", () => {
  it("renders User", () => {
    render(
      <AuthProvider>
        <GuildProvider>
          <User />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("User");

    expect(component).toBeInTheDocument();
  });
});
