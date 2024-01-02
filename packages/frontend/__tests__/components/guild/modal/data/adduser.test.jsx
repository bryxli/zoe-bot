import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import AddUser from "@/components/guild/modal/data/AddUser";

describe("AddUser", () => {
  it("renders AddUser", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <AddUser />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("AddUser");

    expect(component).toBeInTheDocument();
  });
});
