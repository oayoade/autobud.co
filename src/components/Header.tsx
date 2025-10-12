import { Button } from "@/components/ui/button";

export const Header = () => {
  const scrollToContact = () => {
    const contactSection = document.getElementById("contact");
    contactSection?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header className="fixed top-0 right-0 z-50 p-6">
      <Button 
        onClick={scrollToContact}
        size="lg"
        className="bg-[#0EA5E9] hover:bg-[#0EA5E9]/90 text-white font-semibold"
      >
        Let's begin!
      </Button>
    </header>
  );
};
