import { Workflow, Zap, Bot, Network } from "lucide-react";

const services = [
  {
    icon: Workflow,
    title: "n8n Workflows",
    description: "Complex automation workflows that connect your entire tech stack seamlessly.",
  },
  {
    icon: Zap,
    title: "Make & Zapier",
    description: "Rapid automation deployment with industry-leading integration platforms.",
  },
  {
    icon: Bot,
    title: "AI Integration",
    description: "Leverage cutting-edge AI models to enhance your business processes.",
  },
  {
    icon: Network,
    title: "Custom Solutions",
    description: "Tailored automation strategies designed for your unique business needs.",
  },
];

export const Services = () => {
  return (
    <section className="py-24 bg-muted/30">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Our Expertise
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            We specialize in the most powerful automation tools to transform your operations
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-card p-8 rounded-lg shadow-[var(--shadow-card)] hover:shadow-[var(--shadow-glow)] transition-all duration-300 hover:-translate-y-2"
            >
              <div className="w-14 h-14 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center mb-6">
                <service.icon className="w-7 h-7 text-primary-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{service.title}</h3>
              <p className="text-muted-foreground">{service.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
