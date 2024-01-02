import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Setup from "@/components/guild/modal/data/Setup";

describe("Setup", () => {
  it("renders Setup", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Setup />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Setup");

    expect(component).toBeInTheDocument();
  });
});
