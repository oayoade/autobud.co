import { Button } from "@/components/ui/button";
import heroImage from "@/assets/hero-automation.jpg";
import logo from "@/assets/logo.png";

export const Hero = () => {
  const scrollToContact = () => {
    const contactSection = document.getElementById("contact");
    contactSection?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `url(${heroImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          opacity: 0.15,
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background/95 to-background z-[1]" />
      
      <div className="container relative z-10 mx-auto px-6 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="space-y-2">
            <p className="text-xl md:text-2xl font-bold tracking-wide" style={{ color: '#0EA5E9' }}>autobud.co</p>
            <img src={logo} alt="AutoBud Logo" className="w-32 h-32 mx-auto" />
          </div>
          <h1 className="text-5xl md:text-7xl font-bold leading-tight">
            Automate Your Business,{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Amplify Your Growth
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
            We build intelligent automation workflows with n8n, Make, Zapier, and AI—so you can focus on what matters most.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Button 
              size="lg" 
              variant="hero"
              onClick={scrollToContact}
              className="text-lg px-8 py-6"
            >
              Start Your Automation Journey
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              onClick={scrollToContact}
              className="text-lg px-8 py-6"
            >
              Learn More
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};
