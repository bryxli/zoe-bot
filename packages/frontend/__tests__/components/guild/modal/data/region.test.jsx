import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Region from "@/components/guild/modal/data/Region";

describe("Region", () => {
  it("renders Region", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Region />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Region");

    expect(component).toBeInTheDocument();
  });
});
