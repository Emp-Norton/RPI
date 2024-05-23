# sim800l = Sim800l.new('/dev/serial0')
# sim800l.send_sms('+1234567890', 'Hello, world!')
# puts sim800l.read_unread_sms

class Sim800l
  attr_reader :serial_port

  def initialize(serial_port = '/dev/serial0')
    @serial_port = serial_port
  end

  def send_at_command(command, params = {})
    # Custom command method that formats and encodes the AT command
    at_command = "AT+#{command}"
    params.each do |key, value|
      at_command += "#{key}=#{value}&"
    end
    at_command.chomp!('&') # Remove trailing ampersand
    at_command += "\r\n"

    # Send the command over the serial port and get the response
    response = send_serial_command(at_command)

    # Check for errors in the response
    if response.include?('ERROR')
      raise "Error sending AT command: #{response}"
    end

    response
  end

  def send_sms(phone_number, message)
    # Send an SMS message using the SIM800L
    send_at_command('CMGS', '=\"#{phone_number}\"' => nil)
    encoded_message = encode_message(message)
    response = send_serial_command("#{encoded_message}\r\n")
    if response.include?('ERROR')
      raise "Error sending SMS: #{response}"
    end
    response
  end

  def read_unread_sms
    # Read unread SMS messages from the SIM800L
    response = send_at_command('CMGL', '=\"REC UNREAD\"' => nil)
    if response.include?('ERROR')
      raise "Error reading unread SMS: #{response}"
    end
    response
  end

  private

  def send_serial_command(command)
    # Open the serial port and send the command
    begin
      serial = open(serial_port, 'w+')
      serial.write(command)
      response = serial.read
      serial.close
      response
    rescue => e
      raise "Error communicating with serial port: #{e.message}"
    end
  end

  def encode_message(message)
    # Encode the message according to the SIM800L's requirements
    encoded_message = ''
    message.each_char do |char|
      encoded_message += char.unpack('H*').first
    end
    encoded_message
  end
end
