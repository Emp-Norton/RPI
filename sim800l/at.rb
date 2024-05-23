# sim800l = Sim800l.new
# sim800l.send_sms('+1234567890', 'Hello, world!')
# unread_messages = sim800l.read_unread_sms_messages
# puts unread_messages

class Sim800l
  attr_reader :serial_port

  def initialize(serial_port = '/dev/serial0')
    @serial_port = serial_port
  end

  # Sends a custom command to the SIM800L
  #
  # @param command [String] The command to send (less the "AT+" and "\r\n")
  # @return [String] The response from the SIM800L
  def custom_command(command)
    send_command("AT+#{command}")
  end

  # Sends an SMS message
  #
  # @param phone_number [String] The phone number to send the message to
  # @param message [String] The message to send
  # @return [String] The response from the SIM800L
  def send_sms(phone_number, message)
    encoded_message = encode_message(message)
    send_command("AT+CMGS=\"#{phone_number}\"\r\n#{encoded_message}")
  end

  # Reads all unread SMS messages
  #
  # @return [Array<String>] An array of unread SMS messages
  def read_unread_sms_messages
    response = send_command('AT+CMGL="REC UNREAD"')
    parse_sms_response(response)
  end

  private

  # Sends a command to the SIM800L
  #
  # @param command [String] The command to send
  # @return [String] The response from the SIM800L
  def send_command(command)
    serial = File.open(serial_port, 'w+')
    serial.puts "#{command}\r\n"
    response = serial.readlines.join
    serial.close

    check_for_errors(response)
  end

  # Encodes a message for sending as an SMS
  #
  # @param message [String] The message to encode
  # @return [String] The encoded message
  def encode_message(message)
    message.bytes.map { |byte| byte.to_s(16).upcase }.join
  end

  # Parses an SMS response from the SIM800L
  #
  # @param response [String] The response to parse
  # @return [Array<String>] An array of SMS messages
  def parse_sms_response(response)
    messages = response.split("\n")
    messages.select { |message| message.start_with? '+CMGL' }.map do |message|
      message.gsub(/^\+CMGL: \d+,/, '')
    end
  end

  # Checks for errors in a response from the SIM800L
  #
  # @param response [String] The response to check
  # @return [String] The response if no error is found
  # @raise [RuntimeError] If an error is found in the response
  def check_for_errors(response)
    return response unless response.include?('ERROR')

    error_message = response.gsub(/ERROR: /, '')
    raise "SIM800L Error: #{error_message}"
  end
end
