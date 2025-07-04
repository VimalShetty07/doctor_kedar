export default function ServicesSection() {
  const services = [
    {
      title: "Advanced Bronchoscopy",
      description: "Rigid & Flexible bronchoscopy procedures for precise lung diagnosis and treatment planning with state-of-the-art imaging technology.",
      icon: "🫁",
      gradient: "from-blue-500 to-blue-600",
      bgGradient: "from-blue-50 to-blue-100",
      features: ["Rigid Bronchoscopy", "Flexible Bronchoscopy", "Real-time Imaging"]
    },
    {
      title: "Endobronchial Ultrasound (EBUS)",
      description: "TBNA & Transbronchial Cryobiopsy for accurate tissue sampling and comprehensive lung disease diagnosis.",
      icon: "🔬",
      gradient: "from-teal-500 to-teal-600",
      bgGradient: "from-teal-50 to-teal-100",
      features: ["EBUS-TBNA", "Cryobiopsy", "Tissue Analysis"]
    },
    {
      title: "Airway Interventions",
      description: "Cryotherapy, APC, Laser Therapy, Balloon Dilation & Airway Stenting for complex airway tumors and obstructions.",
      icon: "⚕️",
      gradient: "from-purple-500 to-purple-600",
      bgGradient: "from-purple-50 to-purple-100",
      features: ["Laser Therapy", "Balloon Dilation", "Airway Stenting"]
    },
    {
      title: "Lung Cancer Diagnosis",
      description: "Comprehensive thoracic oncology care with cutting-edge diagnostic and personalized treatment solutions.",
      icon: "🎯",
      gradient: "from-red-500 to-red-600",
      bgGradient: "from-red-50 to-red-100",
      features: ["Early Detection", "Staging", "Treatment Planning"]
    },
    {
      title: "Interstitial Lung Diseases",
      description: "Expert diagnosis and management of complex lung conditions, pulmonary fibrosis, and rare respiratory disorders.",
      icon: "📊",
      gradient: "from-green-500 to-green-600",
      bgGradient: "from-green-50 to-green-100",
      features: ["ILD Diagnosis", "Pulmonary Function", "Treatment Plans"]
    },
    {
      title: "Therapeutic Thoracoscopy",
      description: "Minimally invasive procedures including pleuroscopy and IPC placement for pleural conditions and lung diseases.",
      icon: "🔧",
      gradient: "from-orange-500 to-orange-600",
      bgGradient: "from-orange-50 to-orange-100",
      features: ["Pleuroscopy", "IPC Placement", "Pleural Biopsy"]
    }
  ]

  return (
    <section id="services" className="section-padding bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-soft"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-teal-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-soft"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-fade-in">
          <div className="inline-block bg-gradient-to-r from-blue-600 to-teal-500 text-white px-6 py-2 rounded-full text-sm font-semibold mb-4">
            Advanced Medical Services
          </div>
          <h2 className="section-title text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Specialized <span className="text-gradient">Pulmonology Services</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Comprehensive respiratory care services with advanced interventional pulmonology 
            procedures designed to provide precise diagnosis and effective treatment for lung diseases.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {services.map((service, index) => (
            <div 
              key={index} 
              className="group card-gradient p-8 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 animate-fade-in"
              style={{animationDelay: `${index * 0.1}s`}}
            >
              {/* Service Icon */}
              <div className="relative mb-6">
                <div className={`absolute inset-0 bg-gradient-to-r ${service.bgGradient} rounded-2xl scale-110 opacity-50 group-hover:scale-125 transition-transform duration-500`}></div>
                <div className="relative w-16 h-16 mx-auto bg-white rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <span className="text-3xl medical-icon">{service.icon}</span>
                </div>
              </div>
              
              {/* Content */}
              <h3 className="text-xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors duration-300">
                {service.title}
              </h3>
              <p className="text-gray-600 leading-relaxed mb-6">
                {service.description}
              </p>
              
              {/* Features */}
              <div className="space-y-2 mb-6">
                {service.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex items-center text-sm text-gray-700">
                    <div className={`w-2 h-2 bg-gradient-to-r ${service.gradient} rounded-full mr-3 group-hover:scale-125 transition-transform duration-300`}></div>
                    {feature}
                  </div>
                ))}
              </div>
              
              {/* CTA */}
              <div className={`h-1 bg-gradient-to-r ${service.gradient} rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500`}></div>
            </div>
          ))}
        </div>
        
      </div>
    </section>
  )
} 