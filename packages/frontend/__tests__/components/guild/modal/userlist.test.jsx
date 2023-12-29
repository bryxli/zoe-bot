import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import UserList from "@/components/guild/modal/UserList";

describe("UserList", () => {
  it("renders UserList", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <UserList />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("UserList");

    expect(component).toBeInTheDocument();
  });
});
