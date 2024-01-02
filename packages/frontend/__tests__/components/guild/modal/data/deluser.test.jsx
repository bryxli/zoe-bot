import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import DelUser from "@/components/guild/modal/data/DelUser";

describe("DelUser", () => {
  it("renders DelUser", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <DelUser />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("DelUser");

    expect(component).toBeInTheDocument();
  });
});
