import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Modal from "@/components/guild/Modal";

describe("Modal", () => {
  it("renders Modal", () => {
    render(
      <AuthProvider>
        <GuildProvider>
          <Modal />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Modal");

    expect(component).toBeInTheDocument();
  });
});
