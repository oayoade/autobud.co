import logo from "@/assets/logo.png";

export const Footer = () => {
  return (
    <footer className="border-t py-12">
      <div className="container mx-auto px-6">
        <div className="text-center space-y-4">
          <img src={logo} alt="AutoBud Logo" className="w-16 h-16 mx-auto" />
          <h3 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            AutoBud
          </h3>
          <p className="text-muted-foreground">
            Automation experts for the modern business
          </p>
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} AutoBud. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
